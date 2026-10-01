#!/usr/bin/env python3
"""Record command-driven workflow steps without additional confirmation gates."""

import argparse
import copy
import json
from pathlib import Path
from datetime import datetime, timezone

from record_gate import (ROOT, atomic_write, context, digest, prepare_transition,
                         read_json, require, run_lock, validate_prompt, writable,
                         validate_flow, audit_evidence, validate_repair_authorization)


def approve_prompt(run, path, prompt, dry_run):
    require(run.get("gates", {}).get("current") == "prompt",
            "prompt close is out of order")
    config_ref = run["experiment_configuration"]
    config = writable(ROOT / config_ref["artifact"])
    require(digest(config.read_bytes()) == config_ref["checksum"], "configuration checksum mismatch")
    result = validate_prompt(config, run["uc_id"], run["run_id"], prompt, allow_draft=True)
    raw = prompt.read_bytes()
    # Only frontmatter status changes; prompt content and configured boundaries remain intact.
    import re
    front = re.match(rb"\A(?:\xef\xbb\xbf)?---\r?\n.*?\r?\n---(?:\r?\n|$)", raw, re.S)
    require(front is not None, "prompt needs frontmatter")
    header, count = re.subn(rb"(?m)^(status:[ \t]*)(?:Draft|'Draft'|\"Draft\")([ \t]*\r?)$",
                            rb"\1Approved\2", front[0])
    if count == 0:
        # Keep previously approved bytes, including BOM/line endings, immutable.
        validate_prompt(config, run["uc_id"], run["run_id"], prompt)
    approved = header + raw[front.end():]
    folder = ROOT / "docs/02-construction/implementation" / run["uc_id"] / "runs" / run["run_id"]
    snapshot = folder / "approved-prompt" / prompt.name
    if snapshot.exists():
        require(snapshot.read_bytes() == approved, "run-local approved prompt is immutable")
    if not dry_run:
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(approved)
        validate_prompt(config, run["uc_id"], run["run_id"], snapshot)
        prompt.write_bytes(approved)
        run["coding_prompt"] = {"path": snapshot.relative_to(ROOT).as_posix(), "sha256": digest(approved)}
        run["prompt_variant"] = result["prompt_variant"]
        atomic_write(path, run)
    return {"action": "approve_prompt", "prompt": prompt.relative_to(ROOT).as_posix()}


def prepare(run, folder, action, turn_id):
    updated = copy.deepcopy(run)
    receipts = []
    mapping = {"prompt-close": ("prompt", "confirmed"), "source-close": ("source", "confirmed"),
               "audit": ("first_pass_audit", "confirmed"), "repair": ("repair_decision", "authorized"),
               "repair-close": ("repair", "confirmed"), "finalize": ("final_metrics", "confirmed")}
    gate, outcome = mapping[action]
    current = updated["gates"]["current"]
    if action == "repair":
        require(updated.get("run_status") not in {"complete", "blocked", "stopped", "repair_declined"}
                and (updated.get("metrics") or {}).get("status") != "finalized",
                "repair cannot reopen a terminal run")
    if action == "repair-close" and current == "final_metrics":
        require(not updated.get("repairs") and updated.get("repair_skip_reason"), "missing no-repair evidence")
        audit_evidence(updated, folder, "initial")
        return updated, {"action": action, "status": "skipped", "receipts": []}
    # An already persisted command is a replay, never a new confirmation or repair cycle.
    prior = next((r for r in updated["gates"]["history"] if r["gate"] == gate), None)
    if prior:
        require(prior["outcome"] == outcome, "conflicting recorded command outcome")
        if action == "repair":
            validate_repair_authorization(updated)
        return updated, {"action": action, "status": "already_recorded", "receipts": []}
    receipts.append(prepare_transition(updated, folder, gate, outcome, turn_id))
    if action == "audit":
        business = updated["business_rules"]["initial"]
        counts = validate_flow(updated, folder)["counts"]
        if business["met"] == business["total"] and counts["correct"] == counts["total"]:
            updated["business_rules"]["final"] = copy.deepcopy(business)
            receipts.append(prepare_transition(updated, folder, "repair_decision", "skipped", turn_id,
                                                "All frozen BRs and flows pass; repair unnecessary."))
    for receipt in receipts:
        receipt["command_action"] = action
        receipt["recorded_at"] = receipt.pop("confirmed_at")
    return updated, {"action": action, "status": "recorded", "receipts": receipts,
                     "next_step": updated["gates"]["current"]}


def prompt_activation(run, folder, turn_id):
    """Build/validate activation during prompt close, before source generation."""
    from record_gate import closed_phase
    closed_phase(run, "prompt_generation")
    config_ref = run["experiment_configuration"]
    config = writable(ROOT / config_ref["artifact"])
    require(digest(config.read_bytes()) == config_ref["checksum"], "configuration checksum mismatch")
    prompt = writable(ROOT / run["coding_prompt"]["path"])
    require(digest(prompt.read_bytes()) == run["coding_prompt"]["sha256"], "approved prompt checksum mismatch")
    path = folder / "run-activation.json"
    result = validate_prompt(config, run["uc_id"], run["run_id"], prompt,
                             activation=path if path.exists() else None)
    if path.exists():
        return path, None  # Existing valid receipts remain byte-for-byte unchanged.
    return path, {
        "artifact_type": "run-activation", "gate_version": 5,
        "uc_id": run["uc_id"], "run_id": run["run_id"], "prompt_variant": result["prompt_variant"],
        "configuration_artifact": config_ref["artifact"], "configuration_checksum": config_ref["checksum"],
        "activated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "Confirmed", "approved_prompt": result["prompt"],
        "created_by": "measure_prompt_close", "prompt_close_turn_id": turn_id,
    }


def commit(path, updated, folder, action, turn_id):
    """Commit derived receipt then canonical step; replay can recover interrupted writes."""
    if action == "prompt-close":
        activation, receipt = prompt_activation(updated, folder, turn_id)
        if receipt is not None:
            atomic_write(activation, receipt)
        updated["experiment_configuration"]["run_activation"] = activation.relative_to(ROOT).as_posix()
    atomic_write(path, updated)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-json", required=True, type=Path)
    parser.add_argument("--action", required=True, choices=("approve-prompt", "prompt-close", "source-close",
                                                          "audit", "repair", "repair-close", "finalize"))
    parser.add_argument("--turn-id", required=True)
    parser.add_argument("--prompt", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path, run, folder = context(args.run_json)
    require(args.turn_id.strip(), "actual command turn ID required")
    with run_lock(folder):
        run = read_json(path)
        if args.action == "approve-prompt":
            require(args.prompt is not None, "--prompt required for prompt approval")
            result = approve_prompt(run, path, writable(args.prompt), args.dry_run)
        else:
            updated, result = prepare(run, folder, args.action, args.turn_id)
            if args.action == "prompt-close":
                prompt_activation(updated, folder, args.turn_id)
            if not args.dry_run and (updated != run or args.action == "prompt-close"):
                commit(path, updated, folder, args.action, args.turn_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"workflow command error: {exc}")
