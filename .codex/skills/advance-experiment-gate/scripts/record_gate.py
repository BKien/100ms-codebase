#!/usr/bin/env python3
"""Persist one validated experiment gate transition after its internal action succeeds."""

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "measure-uc-workflow/scripts"))
from metrics_contract import ROOT, atomic_write, context, digest, read_json, require, run_lock, validate_metrics, writable
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "gen-coding-prompt/scripts"))
from validate_prompt_contract import validate_prompt, normalize_variant, validate_configuration
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "audit-generation-metrics/scripts"))
from calculate_metrics import terminal_assessment_stage, validate_flow, validate_snapshot
from flow_summary import accepted_summary

AUTO_REPAIR_POLICY = "flow-followup-auto-repair-v1"
AUTO_REPAIR_REFERENCE = "docs/00-context/workflow/gates/FLOW-FOLLOWUP-AUTO-REPAIR.md"

NEXT = {
    "prompt": {"confirmed": "source"},
    "source": {"confirmed": "first_pass_audit"},
    "first_pass_audit": {"confirmed": "repair_decision"},
    "repair_decision": {"authorized": "repair", "skipped": "final_metrics"},
    "repair": {"confirmed": "final_metrics"},
    "final_metrics": {"confirmed": None},
}

def validate_gate_history(gates, gate):
    history = gates.get("history")
    require(isinstance(history, list), "invalid gate history")
    possible = {"prompt"}
    for row in history:
        require(isinstance(row, dict), "invalid gate receipt")
        prior = row.get("gate")
        require(prior in possible, "invalid gate sequence")
        possible = {NEXT[prior][row["outcome"]]} if row.get("outcome") in NEXT.get(prior, {}) else set()
        require(possible, "invalid gate outcome")
    current = gates.get("current")
    require(current in possible, "gate history does not reach current gate")
    require(current == gate, "gate is not current")
    return history


def snapshot_hash(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def closed_phase(run, phase):
    metrics = run.get("metrics")
    require(isinstance(metrics, dict), "gate requires persisted telemetry")
    validate_metrics(metrics)
    require(all(metrics.get(k) == run[k] for k in ("uc_id", "run_id")), "telemetry identity mismatch")
    require(metrics.get("phases", {}).get(phase, {}).get("status") == "closed", f"{phase} telemetry must be closed")


def audit_evidence(run, folder, stage):
    business = run.get("business_rules") or {}
    ordered = business.get("ordered_br_ids")
    require(isinstance(ordered, list) and ordered and len(ordered) == len(set(ordered)), "BR baseline IDs required")
    baseline = read_json(writable(ROOT / business.get("baseline", "")))
    require(baseline.get("status") == "Frozen" and baseline.get("uc_id") == run["uc_id"]
            and baseline.get("ordered_br_ids") == ordered, "BR baseline mismatch")
    snapshot = business.get(stage)
    validated = copy.deepcopy(snapshot)
    validate_snapshot(validated, ordered, f"business_rules.{stage}")
    require(validated == snapshot, "persist validated BR counts before closing Audit Gate")
    summary = validate_flow(run, folder)
    block = run["flow_accuracy"]
    current = next(r for r in block["assessments"] if r["assessment_id"] == block["current_assessment_id"])
    require(current.get("stage") == stage, f"gate requires {stage} flow assessment")
    require(all(current["input"].get(k) == run[k] for k in ("uc_id", "run_id")), "audit identity mismatch")
    source = current["input"].get("source_revision")
    require(isinstance(source, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", source), "audited source hash required")
    if stage == "final":
        require(source == business.get("source_revision"), "final BR/flow source hash mismatch")
    evidence = {"business_rules_sha256": snapshot_hash(snapshot), "flow_assessment_id": summary["assessment_id"],
                "flow_assessment_sha256": snapshot_hash(current), "source_revision": source}
    if block.get("current_summary") is not None:
        evidence["flow_progress_sha256"] = snapshot_hash(block["current_summary"])
        evidence["flow_followup_ids"] = summary["followup_ids"]
        evidence["flow_result_basis"] = summary["result_basis"]
        if summary.get("selection_policy"):
            evidence["flow_selection_policy"] = summary["selection_policy"]
            evidence["flow_assessment_ids"] = [a["assessment_id"] for a in block["assessments"]]
    return evidence


def validate_repair_authorization(run):
    """Validate authorization recorded by the researcher repair command."""
    decision = next((r for r in run.get("gates", {}).get("history", [])
                     if r.get("gate") == "repair_decision"), None)
    approval = run.get("repair_authorization") or {}
    require(decision and decision["outcome"] == "authorized" and approval.get("approved") is True
            and approval.get("turn_id") == decision["turn_id"], "repair authorization mismatch")
    require(approval.get("mode", "researcher") == "researcher", "repair requires an explicit researcher command")
    require(decision.get("automatic_decision") is None, "repair requires an explicit researcher command")
    return approval


def automatic_context(run, folder, followup_id, source_revision):
    """Read validated persisted results; unknown evidence is never a repair defect."""
    require(run.get("run_status") not in {"complete", "blocked", "stopped", "repair_declined"}
            and (run.get("metrics") or {}).get("status") != "finalized",
            "automatic continuation cannot reopen a terminal run")
    require(not run.get("repairs"), "automatic continuation cannot restart executed repairs")
    require((run.get("metrics") or {}).get("phases", {}).get("repair", {}).get("status") != "closed",
            "automatic continuation cannot reopen closed repair telemetry")
    closed_phase(run, "source_generation")
    evidence = audit_evidence(run, folder, "initial")
    require(source_revision == evidence["source_revision"]
            == run["business_rules"].get("source_revision"),
            "current source differs from initial audit; inspect drift before repair")
    followups = run["flow_accuracy"].get("followups", [])
    require(followups and followups[-1]["followup_id"] == followup_id,
            "automatic continuation requires the latest saved follow-up")
    followup = followups[-1]
    require(followup.get("results"), "a summary refresh is not an automatic repair trigger")
    summary = validate_flow(run, folder)
    require(summary.get("selection_policy") == "accepted-audit-results-v1",
            "automatic continuation requires accepted flow results")
    require(all(f["source_revision"] == source_revision for f in summary["flows"]
                if f["status"] != "not_evaluable"),
            "accepted results belong to older source; inspect current defects first")
    business = run["business_rules"]["initial"]
    br_ids = [r["br_id"] for r in business["requirements"] if r["status"] == "unmet"]
    flow_ids = [r["flow_id"] for r in summary["flows"] if r["status"] == "incorrect"]
    outcome = "authorized" if br_ids or flow_ids else (
        "skipped" if business["met"] == business["total"]
        and summary["counts"]["correct"] == summary["counts"]["total"] else None)
    if summary["counts"].get("not_evaluable", 0):
        outcome = None
    context = {"policy_id": AUTO_REPAIR_POLICY, "policy_artifact": AUTO_REPAIR_REFERENCE,
               "policy_sha256": digest((ROOT / AUTO_REPAIR_REFERENCE).read_bytes()),
               "followup_id": followup_id, "followup_sha256": snapshot_hash(followup),
               "source_revision": source_revision, "defect_br_ids": br_ids, "defect_flow_ids": flow_ids}
    return outcome, context


def prepare_transition(run, folder, gate, outcome, turn_id, reason=None, automatic=None):
    """Validate the common pipeline and its evidence; mutate only the in-memory copy."""
    require(gate in NEXT and outcome in NEXT[gate], "invalid gate/outcome")
    gates = run.get("gates")
    require(isinstance(gates, dict), "gate state required")
    history = validate_gate_history(gates, gate)
    if automatic is not None:
        require(gate == "repair_decision", "automatic policy applies only to Repair Decision")
        selected, validated = automatic_context(run, folder, automatic["followup_id"], automatic["source_revision"])
        require(selected == outcome and validated == automatic, "automatic decision differs from current evidence")
        require(outcome == "skipped", "follow-up can record a skip; repair needs an explicit command")
    require(isinstance(turn_id, str) and turn_id.strip(), "actual gate decision turn ID required")
    require(not any(r.get("gate") == gate for r in history), "workflow step already recorded")
    config_ref = run.get("experiment_configuration") or {}
    config_path = writable(ROOT / config_ref.get("artifact", ""))
    require(config_path.is_file() and digest(config_path.read_bytes()) == config_ref.get("checksum"), "configuration checksum mismatch")
    config = validate_configuration(config_path)
    assignments = [r for r in config["runs"] if r.get("uc_id") == run["uc_id"] and r.get("run_id") == run["run_id"]]
    require(len(assignments) == 1, "gate needs configured UC/run")
    variant = normalize_variant(assignments[0].get("prompt_variant"))
    require(normalize_variant(run.get("prompt_variant")) == variant, "canonical run/configuration variant mismatch")
    if gate != "prompt" and (folder / "run-activation.json").is_file():
        activation = read_json(folder / "run-activation.json")
        require(activation.get("uc_id") == run["uc_id"] and activation.get("run_id") == run["run_id"]
                and activation.get("status") == "Confirmed", "gate activation mismatch")
        require(activation.get("configuration_artifact") == config_ref["artifact"]
                and activation.get("configuration_checksum") == config_ref["checksum"], "activation/configuration mismatch")
        require(normalize_variant(activation.get("prompt_variant")) == variant, "gate activation variant mismatch")
    evidence = {}
    if gate in {"prompt", "source"}:
        reference = run.get("coding_prompt") or {}
        prompt = writable(ROOT / reference.get("path", ""))
        require(prompt.is_file() and digest(prompt.read_bytes()) == reference.get("sha256"), "approved coding_prompt reference required")
        result = validate_prompt(config_path, run["uc_id"], run["run_id"], prompt,
                                 folder / "run-activation.json" if gate == "source" and (folder / "run-activation.json").is_file() else None)
        require(normalize_variant(run.get("prompt_variant")) == result["prompt_variant"], "run/prompt variant mismatch")
        closed_phase(run, "prompt_generation" if gate == "prompt" else "source_generation")
        evidence["coding_prompt"] = reference
    if gate in {"first_pass_audit", "repair_decision", "repair", "final_metrics"}:
        closed_phase(run, "source_generation")
    if gate in {"first_pass_audit", "repair", "final_metrics"}:
        stage = "initial" if gate == "first_pass_audit" else ("final" if gate == "repair" else terminal_assessment_stage(run))
        evidence = audit_evidence(run, folder, stage)
    if gate in {"repair_decision", "repair", "final_metrics"}:
        first = next((r for r in history if r["gate"] == "first_pass_audit"), None)
        require(first is not None, "first-pass audit must precede repair/finalization")
        recorded = first.get("evidence") or {}
        require(recorded, "first-pass audit evidence is required")
        require(recorded.get("business_rules_sha256") == snapshot_hash(run["business_rules"]["initial"]), "initial BR evidence changed")
        initial = next((r for r in run["flow_accuracy"]["assessments"] if r["assessment_id"] == recorded.get("flow_assessment_id")), None)
        require(initial is not None and snapshot_hash(initial) == recorded.get("flow_assessment_sha256"), "initial flow evidence changed")
        for prior_receipt in history:
            pinned = prior_receipt.get("evidence") or {}
            if "flow_progress_sha256" not in pinned:
                continue
            block = run["flow_accuracy"]
            parent = next((a for a in block["assessments"] if a["assessment_id"] == pinned.get("flow_assessment_id")), None)
            followup_ids = pinned.get("flow_followup_ids", [])
            retained = [r for r in block.get("followups", []) if r["followup_id"] in followup_ids]
            require(parent is not None and [r["followup_id"] for r in retained] == followup_ids,
                    "gate-pinned flow follow-ups missing or reordered")
            require(pinned.get("flow_selection_policy") == "accepted-audit-results-v1", "flow policy required")
            assessment_ids = pinned.get("flow_assessment_ids", [])
            assessments = [a for a in block["assessments"] if a["assessment_id"] in assessment_ids]
            require([a["assessment_id"] for a in assessments] == assessment_ids, "gate-pinned flow assessments changed")
            frozen = {"flow_accuracy": {"assessments": assessments, "followups": retained,
                                       "current_assessment_id": parent["assessment_id"]}}
            projection = accepted_summary(frozen)
            require(projection["selection_policy"] == pinned["flow_selection_policy"], "gate flow policy changed")
            require(snapshot_hash(projection) == pinned["flow_progress_sha256"],
                    "gate-pinned flow progress changed")
    if gate == "repair_decision":
        initial_evidence = audit_evidence(run, folder, "initial")
        if outcome == "authorized":
            summary = validate_flow(run, folder)
            require(summary["counts"].get("not_evaluable", 0) == 0,
                    "repair requires conclusive accepted results for every frozen flow; save missing researcher results or complete measurement first")
            require(any(r["status"] == "unmet" for r in run["business_rules"]["initial"]["requirements"])
                    or summary["counts"]["incorrect"] > 0, "repair requires an evidenced defect")
        if automatic is not None:
            evidence = initial_evidence
        if outcome == "skipped":
            require(isinstance(reason, str) and reason.strip(), "skip requires the actual decision reason")
            require(not run.get("repairs"), "cannot skip already executed repair")
            run["repair_skip_reason"] = reason
            # Final values are the same observation, not a fabricated second audit.
            initial_evidence = audit_evidence(run, folder, "initial")
            require(run["business_rules"].get("source_revision") == initial_evidence["source_revision"],
                    "no-repair decision requires the unchanged audited source hash")
            require(run["business_rules"].get("final") == run["business_rules"]["initial"],
                    "no-repair decision requires unchanged BR results")
            evidence = initial_evidence
            if run.get("run_status") not in {"blocked", "stopped", "repair_declined"}:
                initial = run["business_rules"]["initial"]
                flow = validate_flow(run, folder)["counts"]
                verified = (initial["met"] == initial["total"] and flow["correct"] == flow["total"])
                run["run_status"] = "complete" if verified else "repair_declined"
        run["repair_authorization"] = {"approved": outcome == "authorized", "turn_id": turn_id}
        if automatic is not None:
            run["repair_authorization"].update(mode="automatic_policy", automatic_decision=automatic)
    if gate == "repair":
        validate_repair_authorization(run)
        closed_phase(run, "repair")
    if gate == "final_metrics":
        require(run.get("metrics", {}).get("status") == "finalized", "final workflow metrics must be persisted")
    receipt = {"gate": gate, "outcome": outcome, "turn_id": turn_id,
               "confirmed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    if automatic is not None:
        receipt["decided_at"] = receipt.pop("confirmed_at")
        receipt["automatic_decision"] = automatic
    if evidence:
        receipt["evidence"] = evidence
    if gate == "repair_decision" and outcome == "skipped":
        receipt["reason"] = reason
    history.append(receipt)
    gates["current"] = NEXT[gate][outcome]
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-json", required=True, type=Path)
    parser.add_argument("--gate", required=True, choices=NEXT)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--turn-id", required=True)
    parser.add_argument("--reason", help="Researcher's recorded reason when skipping repair")
    parser.add_argument("--dry-run", action="store_true", help="Validate the pending transition without writing")
    args = parser.parse_args()
    path, _, folder = context(args.run_json)
    require(args.outcome in NEXT[args.gate], "invalid outcome for gate")
    if args.dry_run:
        run = read_json(path)
        prepare_transition(run, folder, args.gate, args.outcome, args.turn_id, args.reason)
        print(json.dumps({"status": "valid", "next_gate": run["gates"]["current"]}, indent=2))
        return
    with run_lock(folder):
        run = read_json(path)
        receipt = prepare_transition(run, folder, args.gate, args.outcome, args.turn_id, args.reason)
        gates = run["gates"]
        atomic_write(path, run)
    print(json.dumps({"status": "closed", "receipt": receipt, "next_gate": gates["current"]}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"gate error: {exc}")
