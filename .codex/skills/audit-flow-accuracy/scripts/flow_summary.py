"""Flow-only progress and append-only follow-ups; original assessments stay immutable."""

import json
import re

from metrics_contract import digest, epoch, require

RESULT_POLICY = "accepted-audit-results-v1"


def fingerprint(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def current_assessment(run):
    block = run.get("flow_accuracy") or {}
    matches = [a for a in block.get("assessments", [])
               if a.get("assessment_id") == block.get("current_assessment_id")]
    require(len(matches) == 1, "current flow assessment must resolve exactly once")
    return matches[0]


def pending_details(flow, assessment):
    targets = [{"target_id": s["step_id"], "reason": s["rationale"]}
               for s in flow["steps"] if s["completion_critical"] and s["status"] == "not_evaluable"]
    outcome = flow["terminal_outcome"]
    if outcome["status"] == "not_evaluable":
        targets.append({"target_id": "terminal_outcome", "reason": outcome["rationale"]})
    if not targets:
        targets.append({"target_id": "completion_observation",
                        "reason": "Connected runtime completion has not been established."})
    return {"flow_id": flow["flow_id"], "missing_targets": targets,
            "limitations": assessment["input"].get("limitations", []),
            "attempts": [{k: o[k] for k in ("observation_id", "state", "end_state")}
                         for o in assessment["input"].get("observations", []) if o["flow_id"] == flow["flow_id"]],
            "resolution_options": ["researcher_result", "llm_measurement"]}


def summary_from_rows(assessment, flows, pending_inputs, applied):
    total = len(flows)
    require(total > 0 and assessment["counts"]["total"] == total, "flow inventory/count mismatch")
    require(all(f["status"] in {"correct", "incorrect", "not_evaluable"} for f in flows), "invalid flow status")
    correct = sum(f["status"] == "correct" for f in flows)
    incorrect = sum(f["status"] == "incorrect" for f in flows)
    evaluated = correct + incorrect
    unknown = total - evaluated
    manual = sum(f["result_source"] == "researcher_result" and f["status"] != "not_evaluable" for f in flows)
    pending = [pending_details(*pending_inputs[f["flow_id"]]) for f in flows if f["status"] == "not_evaluable"]
    return {"schema_version": 2, "assessment_id": assessment["assessment_id"], "stage": assessment["stage"],
            "source_revision": assessment["input"]["source_revision"],
            "rubric_id": assessment["input"]["rubric_id"],
            "followup_ids": applied, "status": "partial" if unknown and evaluated else
            ("not_evaluable" if unknown else ("repair_required" if incorrect else "scored")),
            "measurement_status": "partial" if unknown and evaluated else ("not_evaluable" if unknown else "complete"),
            "has_incorrect_flows": bool(incorrect),
            "result_basis": "includes_researcher_results" if manual else "rubric_evidence",
            "researcher_result_count": manual,
            "counts": {**{k: assessment["counts"][k] for k in ("main", "alternative", "exception", "total")},
                       "correct": correct, "incorrect": incorrect, "not_evaluable": unknown, "evaluated": evaluated},
            "flow_accuracy_percent": round(100 * correct / total, 6) if not unknown else None,
            "flow_error_percent": round(100 * incorrect / total, 6) if not unknown else None,
            "evaluated_accuracy_percent": round(100 * correct / evaluated, 6) if evaluated else None,
            "evaluated_error_percent": round(100 * incorrect / evaluated, 6) if evaluated else None,
            "evaluated_coverage_percent": round(100 * evaluated / total, 6),
            "accuracy_lower_bound_percent": round(100 * correct / total, 6),
            "accuracy_upper_bound_percent": round(100 * (correct + unknown) / total, 6),
            "flows": flows, "pending_flows": pending}


def accepted_summary(run):
    """Report the latest conclusive verdict per flow across audit stages.

    An inconclusive later attempt remains evidence but cannot erase a verdict.
    Stage/source on every selected row identifies the actual observed revision.
    """
    block = run["flow_accuracy"]
    current = current_assessment(run)
    inventory = [(f["flow_id"], f["type"]) for f in current["flows"]]
    parents = {a["assessment_id"]: a for a in block["assessments"]}
    events = []
    for assessment in block["assessments"]:
        require(assessment["input"]["baseline"] == current["input"]["baseline"], "report baseline changed")
        require([(f["flow_id"], f["type"]) for f in assessment["flows"]] == inventory, "report flow inventory changed")
        events.append((epoch(assessment["input"]["captured_at"]), assessment["assessment_id"],
                       "assessment", assessment, assessment["flows"]))
    for record in block.get("followups", []):
        parent = parents[record["assessment_id"]]
        evidence = record.get("runtime_result", parent)
        events.append((epoch(record["recorded_at"]), record["followup_id"], record["mode"], evidence, record["results"]))
    # Stable ordering preserves append order for equal timestamps; follow-ups follow assessments.
    events.sort(key=lambda event: event[0])
    selected, pending_inputs = {}, {}
    applied = [r["followup_id"] for r in block.get("followups", [])]
    for _, identity, mode, evidence, results in events:
        for result in results:
            flow_id = result["flow_id"]
            previous = selected.get(flow_id)
            if result["status"] == "not_evaluable" and previous and previous["status"] != "not_evaluable":
                continue
            original = next(f for f in evidence["flows"] if f["flow_id"] == flow_id)
            selected[flow_id] = {"flow_id": flow_id, "type": original["type"], "status": result["status"],
                                 "result_source": mode, "record_id": identity,
                                 "assessment_id": evidence["assessment_id"], "stage": evidence["stage"],
                                 "source_revision": evidence["input"]["source_revision"]}
            pending_inputs[flow_id] = (original, evidence)
    rows = [selected[flow_id] for flow_id, _ in inventory]
    summary = summary_from_rows(current, rows, pending_inputs, applied)
    summary.update(schema_version=2, selection_policy=RESULT_POLICY,
                   result_scope="experiment_accepted_audit", stage="experiment", source_revision=None,
                   current_source_revision=current["input"]["source_revision"],
                   latest_assessment_status=current["status"], latest_assessment_counts=current["counts"],
                   retained_from_prior_source_count=sum(r["source_revision"] != current["input"]["source_revision"]
                                                        and r["status"] != "not_evaluable" for r in rows))
    return summary


def refresh_report(path, run):
    """Refresh an existing derived report after the canonical write; retry is safe."""
    import subprocess
    import sys
    from metrics_contract import ROOT, writable
    report = writable(ROOT / run["report_artifact"]) if run.get("report_artifact") else path.with_suffix(".md")
    if report.exists() and run.get("run_status") in {"complete", "blocked", "stopped", "repair_declined"}:
        renderer = ROOT / ".codex/skills/render-experiment-report/scripts/render_report.py"
        subprocess.run([sys.executable, "-B", str(renderer), str(path), "--output", str(report)], check=True)


def validate_followups(run, folder):
    # Lazy imports avoid a scorer/projection import cycle.
    from score_flow_accuracy import calculate, validate_evidence
    from runtime_contract import configured_rubric, method
    block = run["flow_accuracy"]
    policy = block.get("selection_policy")
    require(policy == RESULT_POLICY, "unknown flow result selection policy")
    history = block.get("followups", [])
    require(isinstance(history, list), "invalid flow follow-up history")
    assessments = {a["assessment_id"]: a for a in block["assessments"]}
    accepted, ids = [], set()
    for record in history:
        require(isinstance(record, dict) and record.get("schema_version") == 2, "invalid follow-up schema")
        identity = record.get("followup_id")
        require(isinstance(identity, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", identity), "unsafe follow-up ID")
        require(identity not in ids, "duplicate follow-up ID")
        ids.add(identity)
        parent = assessments.get(record.get("assessment_id"))
        require(parent is not None and record.get("assessment_sha256") == fingerprint(parent), "follow-up parent changed")
        for key in ("uc_id", "run_id", "stage", "source_revision", "baseline"):
            require(record.get(key) == parent["input"].get(key), f"follow-up {key} mismatch")
        require(all(record[k] == run[k] for k in ("uc_id", "run_id")), "follow-up run mismatch")
        require(record.get("source_unchanged") is True, "flow follow-up cannot change source")
        require(record.get("mode") in {"researcher_result", "llm_measurement"}, "choose a follow-up mode")
        require(isinstance(record.get("request_turn_id"), str) and record["request_turn_id"].strip(), "researcher request turn required")
        recorded = epoch(record.get("recorded_at"))
        prior = [r for r in accepted if r["assessment_id"] == record["assessment_id"]]
        previous_end = max([epoch(parent["input"]["captured_at"])] + [epoch(r["recorded_at"]) for r in prior])
        require(recorded >= previous_end, "follow-up predates previous results")
        parent_index = block["assessments"].index(parent)
        if parent_index + 1 < len(block["assessments"]) and not (
                record["mode"] == "researcher_result"):
            require(recorded <= epoch(block["assessments"][parent_index + 1]["input"]["captured_at"]),
                    "follow-up cannot revise a superseded source stage")
        pending = {f["flow_id"] for f in parent["flows"]}
        results = record.get("results")
        require(isinstance(results, list) and results, "nonempty per-flow results required")
        target_ids = [r.get("flow_id") for r in results]
        require(len(target_ids) == len(set(target_ids)) and set(target_ids) <= pending, "results must identify eligible frozen flows exactly once")
        require(all(r.get("status") in {"correct", "incorrect", "not_evaluable"} for r in results), "invalid flow result")
        if record["mode"] == "researcher_result":
            require(isinstance(record.get("researcher_result"), str) and record["researcher_result"].strip(), "researcher result text required")
            require("runtime_result" not in record, "researcher result must not fabricate runtime evidence")
        else:
            measured = record.get("runtime_result")
            require(isinstance(measured, dict) and isinstance(measured.get("input"), dict), "LLM assessment required")
            require(calculate(measured["input"]) == measured, "LLM result differs from evidence/scoring")
            require(method(measured["input"]) == method(parent["input"]), "follow-up rubric changed")
            require(configured_rubric(run, folder, validate_evidence, record["baseline"]) == method(measured["input"])[1], "configuration rubric mismatch")
            for key in ("uc_id", "run_id", "stage", "source_revision", "baseline"):
                require(measured["input"].get(key) == record[key], f"runtime follow-up {key} mismatch")
            require(measured["assessment_id"] == identity, "runtime assessment ID must equal follow-up ID")
            require(identity not in assessments, "follow-up needs a distinct assessment ID")
            require(previous_end <= epoch(measured["input"]["captured_at"]) <= recorded, "runtime capture outside follow-up interval")
            prior_inputs = [a["input"] for a in block["assessments"]] + [r["runtime_result"]["input"] for r in accepted if r["mode"] == "llm_measurement"]
            old_ids = {o["observation_id"] for data in prior_inputs for o in data.get("observations", [])}
            for observation in measured["input"].get("observations", []):
                require(observation["observation_id"] not in old_ids and epoch(observation["started_at"]) > previous_end,
                        "follow-up requires fresh runtime observations")
            scored = {f["flow_id"]: f["status"] for f in measured["flows"]}
            require(all(scored[r["flow_id"]] == r["status"] for r in results), "follow-up verdict mismatch")
        accepted.append(record)
    return accepted_summary(run)


def refresh_summary(run, folder):
    run["flow_accuracy"]["selection_policy"] = RESULT_POLICY
    summary = validate_followups(run, folder)
    run["flow_accuracy"]["current_summary"] = summary
    for key in ("flow_accuracy_percent", "flow_error_percent"):
        run[key] = summary[key]
    run["flow_accuracy_status"] = summary["status"]
    return summary


def markdown(summary):
    def shown(key):
        value = summary[key]
        return "N/A" if value is None else str(value)
    lines = ["# Flow measurement progress", "", f"Assessment: {summary['assessment_id']} ({summary['stage']})",
             f"Source revision: {summary['source_revision']}", f"Status: {summary['status']}",
             f"Result basis: {summary['result_basis']}", f"Known incorrect flows: {summary['counts']['incorrect']}",
             f"Whole-baseline accuracy (%): {shown('flow_accuracy_percent')}",
             f"Evaluated-only accuracy (%): {shown('evaluated_accuracy_percent')}",
             f"Evaluated-only error (%): {shown('evaluated_error_percent')}",
             f"Evaluated coverage (%): {shown('evaluated_coverage_percent')}",
             f"Accuracy bounds (%): {summary['accuracy_lower_bound_percent']}–{summary['accuracy_upper_bound_percent']}",
             "", "| Flow | Result | Source | Record |", "|---|---|---|---|"]
    for flow in summary["flows"]:
        lines.append(f"| {flow['flow_id']} | {flow['status']} | {flow['result_source']} | {flow['record_id']} |")
    for pending in summary["pending_flows"]:
        lines += ["", f"Pending: {pending['flow_id']}"]
        lines += [f"- {t['target_id']}: {t['reason']}" for t in pending["missing_targets"]]
        lines += ["Limitations: " + json.dumps(pending["limitations"], ensure_ascii=False)]
        lines += ["Attempts: " + json.dumps(pending["attempts"], ensure_ascii=False)]
    if summary["pending_flows"]:
        lines += ["", "Researcher chooses the next action:",
                  "1. Researcher supplies per-flow results; the LLM records them and recalculates JSON.",
                  "2. LLM continues bounded measurement and automatically persists validated results.",
                  "Neither choice permits application source changes, fixes, mocks or audit-only endpoints."]
    return "\n".join(lines) + "\n"
