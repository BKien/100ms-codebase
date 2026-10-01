#!/usr/bin/env python3
"""Validate flow observations, calculate completion accuracy, and persist evidence."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "measure-uc-workflow/scripts"))
from metrics_contract import ROOT, atomic_write, context, digest, epoch, read_json, require, run_lock, writable
from runtime_contract import method, configured_rubric, validate_runtime, complete_chain
from flow_summary import refresh_report, refresh_summary

OBSERVATION_STATUSES = {"met", "unmet", "not_evaluable"}
FLOW_TYPES = ("main", "alternative", "exception")
FLOW_PREFIX_TYPES = {"BF": "main", "AF": "alternative", "EF": "exception"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_evidence(item):
    require(isinstance(item, dict) and nonempty(item.get("path")), "evidence path required")
    path = writable(ROOT / item["path"])
    require(path.is_file(), f"missing evidence: {item['path']}")
    require(item.get("sha256") == digest(path.read_bytes()), f"changed evidence: {item['path']}")
    return path


def validate_observation(item, label):
    require(isinstance(item, dict) and item.get("status") in OBSERVATION_STATUSES, f"invalid {label} status")
    require(nonempty(item.get("rationale")), f"{label} rationale required")
    refs = item.get("evidence")
    require(isinstance(refs, list) and refs, f"{label} evidence required")
    for ref in refs:
        validate_evidence(ref)


def source_flow_ids(raw):
    """Extract the ordered flow inventory without interpreting flow semantics."""
    content = raw.decode("utf-8-sig")
    headings = list(re.finditer(r"(?m)^(##|###)\s+([^\r\n]+?)\s*\r?$", content))
    require(headings, "frozen UC flow headings missing")
    scope, result, basic_counts = "", [], {}
    for index, heading in enumerate(headings):
        level, title = heading.group(1), heading.group(2).strip()
        if level == "##":
            variant = re.match(r"(UC-[0-9]+(?:\.[0-9]+)?)\s+UI Variant\b", title, re.I)
            scope = f"{variant.group(1).upper()}/" if variant else ""
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        section = content[heading.end():end]
        if re.fullmatch(r"(?:Basic|Main) Flow", title, re.I):
            count = basic_counts.get(scope, 0) + 1
            basic_counts[scope] = count
            result.append(f"{scope}BF-{count}")
        elif re.fullmatch(r"Alternative Flow", title, re.I):
            result.extend(f"{scope}{value}" for value in re.findall(r"(?m)^(AF-[0-9]+)(?=:)", section))
        elif re.fullmatch(r"Exception Flow", title, re.I):
            result.extend(f"{scope}{value}" for value in re.findall(r"(?m)^(EF-[0-9]+)(?=:)", section))
    require(result and len(result) == len(set(result)), "frozen UC flow IDs missing or duplicated")
    return result


def flow_type(flow_id):
    match = re.fullmatch(r"(?:UC-[0-9]+(?:\.[0-9]+)?/)?(BF|AF|EF)-[0-9]+", flow_id or "")
    require(match is not None, f"invalid flow ID: {flow_id}")
    return FLOW_PREFIX_TYPES[match.group(1)]


def validate_baseline(data):
    expected_fields = {"schema_version", "artifact_type", "status", "uc_id", "use_case_path",
                       "use_case_sha256", "spreadsheet_source", "ordered_flow_ids", "frozen_at"}
    require(set(data) == expected_fields, "invalid flow baseline fields")
    require(data.get("schema_version") == 1 and data.get("artifact_type") == "flow-baseline", "invalid baseline schema")
    require(data.get("status") == "Frozen" and nonempty(data.get("uc_id")), "baseline must be Frozen")
    require(nonempty(data.get("spreadsheet_source")), "flow baseline spreadsheet source missing")
    uc_path = writable(ROOT / data.get("use_case_path", ""))
    require(uc_path.is_file(), "baseline UC path missing")
    raw = uc_path.read_bytes()
    require(data.get("use_case_sha256") == digest(raw), "frozen UC changed")
    epoch(data.get("frozen_at"))
    ids = data.get("ordered_flow_ids")
    require(isinstance(ids, list) and ids and all(nonempty(value) for value in ids), "ordered flow IDs required")
    require(len(ids) == len(set(ids)), "duplicate flow IDs")
    for flow_id in ids:
        flow_type(flow_id)
    require(ids == source_flow_ids(raw), "frozen UC/flow baseline order conflict")
    counts = {kind: sum(flow_type(value) == kind for value in ids) for kind in FLOW_TYPES}
    counts["total"] = len(ids)
    require(counts["main"] > 0, "flow baseline needs a Basic/Main Flow")
    return ids, counts


def assessment_definitions(supplied, ordered_ids):
    """Validate the auditor's UC-derived flow breakdown used by the runtime rubric."""
    require([row.get("flow_id") for row in supplied] == ordered_ids, "assessment flow inventory mismatch")
    definitions, all_steps = [], set()
    for assessed in supplied:
        flow_id = assessed["flow_id"]
        require(nonempty(assessed.get("source_anchor")), f"{flow_id} frozen UC source anchor required")
        steps = assessed.get("steps")
        require(isinstance(steps, list) and steps, f"{flow_id} needs UC-derived steps")
        step_definitions = []
        for step in steps:
            step_id = step.get("step_id")
            require(nonempty(step_id) and step_id.startswith(flow_id + "."), f"invalid step ID for {flow_id}")
            require(step_id not in all_steps, "duplicate step ID")
            all_steps.add(step_id)
            require(nonempty(step.get("text")) and type(step.get("completion_critical")) is bool,
                    f"invalid UC-derived step: {step_id}")
            require(nonempty(step.get("criticality_reason")), f"criticality reason required: {step_id}")
            step_definitions.append({key: step[key] for key in
                                     ("step_id", "text", "completion_critical", "criticality_reason")})
        outcome = assessed.get("terminal_outcome") or {}
        require(nonempty(outcome.get("text")), f"{flow_id} UC-derived terminal outcome required")
        definitions.append({"flow_id": flow_id, "type": flow_type(flow_id),
                            "source_anchor": assessed["source_anchor"], "steps": step_definitions,
                            "terminal_outcome": outcome["text"]})
    return definitions


def calculate(data):
    version, rubric = method(data)
    for key in ("uc_id", "run_id", "assessment_id", "source_revision"):
        require(nonempty(data.get(key)), f"missing {key}")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", data["assessment_id"]), "unsafe assessment ID")
    require(data.get("stage") in ("initial", "final"), "invalid stage")
    require(re.fullmatch(r"sha256:[0-9a-f]{64}", data["source_revision"].lower()), "invalid source revision")
    require(isinstance(data.get("limitations"), list), "limitations list required")
    epoch(data.get("captured_at"))
    baseline_path = validate_evidence(data.get("baseline"))
    baseline = read_json(baseline_path)
    ordered_ids, type_counts = validate_baseline(baseline)
    require(baseline.get("uc_id") == data.get("uc_id"), "baseline UC mismatch")
    supplied = data.get("flows")
    require(isinstance(supplied, list), "flow observations required")
    definitions = assessment_definitions(supplied, ordered_ids)
    attempts, validate_target = validate_runtime(data, definitions, validate_evidence)

    results = []
    for definition, assessed in zip(definitions, supplied):
        outcome = assessed.get("terminal_outcome")
        validate_observation(outcome, f"{definition['flow_id']} outcome")
        validate_target(outcome, "terminal_outcome", definition["flow_id"], True)
        steps = assessed.get("steps")
        require(isinstance(steps, list), "step observations required")
        require([row.get("step_id") for row in steps] == [row["step_id"] for row in definition["steps"]],
                f"step inventory mismatch: {definition['flow_id']}")
        blocking_failure = False
        critical_unknown = False
        deviations = 0
        computed_steps = []
        for step_definition, step in zip(definition["steps"], steps):
            validate_observation(step, step_definition["step_id"])
            critical = step_definition["completion_critical"]
            validate_target(step, step_definition["step_id"], definition["flow_id"], critical)
            blocking_failure = blocking_failure or (critical and step["status"] == "unmet")
            critical_unknown = critical_unknown or (critical and step["status"] == "not_evaluable")
            deviations += int(not critical and step["status"] == "unmet")
            computed_steps.append({**step, "completion_critical": critical})
        chain_complete = complete_chain(assessed, definition, attempts)
        if blocking_failure or outcome["status"] == "unmet":
            status = "incorrect"
        elif critical_unknown or outcome["status"] == "not_evaluable" or not chain_complete:
            status = "not_evaluable"
        else:
            status = "correct"
        results.append({"flow_id": definition["flow_id"], "type": definition["type"], "status": status,
                        "noncritical_deviations": deviations, "terminal_outcome": outcome, "steps": computed_steps})

    total = len(results)
    correct = sum(row["status"] == "correct" for row in results)
    incorrect = sum(row["status"] == "incorrect" for row in results)
    unknown = total - correct - incorrect
    exact = unknown == 0
    return {
        "schema_version": version, "rubric_id": rubric,
        "assessment_id": data["assessment_id"],
        "stage": data["stage"],
        "input_sha256": digest(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()),
        "status": "not_evaluable" if unknown else ("repair_required" if incorrect else "scored"),
        "counts": {**type_counts, "correct": correct, "incorrect": incorrect, "not_evaluable": unknown},
        "flow_error_percent": round(100 * incorrect / total, 6) if exact else None,
        "flow_accuracy_percent": round(100 * (total - incorrect) / total, 6) if exact else None,
        "evaluated_coverage_percent": round(100 * (total - unknown) / total, 6),
        "accuracy_lower_bound_percent": round(100 * correct / total, 6),
        "accuracy_upper_bound_percent": round(100 * (correct + unknown) / total, 6),
        "flows": results,
        "input": data,
    }


def markdown(result):
    counts = result["counts"]
    accuracy = result["flow_accuracy_percent"]
    error = result["flow_error_percent"]
    lines = [f"# Flow accuracy: {result['assessment_id']}", "", f"Status: {result['status']}",
             f"Rubric: {method(result['input'])[1]}",
             f"Source revision: {result['input']['source_revision']}",
             f"Flow accuracy: {str(accuracy) + '%' if accuracy is not None else 'N/A'}",
             f"Flow error: {str(error) + '%' if error is not None else 'N/A'}",
             f"Evaluated coverage: {result['evaluated_coverage_percent']}%",
             f"Accuracy bounds: {result['accuracy_lower_bound_percent']}%–{result['accuracy_upper_bound_percent']}%", "",
             f"Flows: {counts['correct']} correct, {counts['incorrect']} incorrect, "
             f"{counts['not_evaluable']} not evaluable, {counts['total']} total", "",
             "| Flow | Type | Status | Noncritical deviations |", "|---|---|---|---:|"]
    for flow in result["flows"]:
        lines.append(f"| {flow['flow_id']} | {flow['type']} | {flow['status']} | {flow['noncritical_deviations']} |")
    lines.append("")
    for limitation in result["input"]["limitations"]:
        lines.append(json.dumps(limitation, ensure_ascii=False) if isinstance(limitation, dict) else limitation)
    lines.extend(["", "## Observation trace", ""])
    for observation in result["input"]["observations"]:
        lines.append(f"- {observation['observation_id']} / {observation['flow_id']}: "
                     f"{observation['started_at']} to {observation['ended_at']}; {observation['state']}; "
                     f"entry {observation['entry_point']}; end {observation['end_state']}")
        for action in observation["actions"]:
            lines.append(f"  {action['sequence']}. {action['action']} -> {action['actual_result']} "
                         f"({', '.join(action['target_ids'])})")
    lines.extend(["", "Evidence paths, SHA-256 values, target decisions and source findings: companion JSON input."])
    lines.append("")
    return "\n".join(lines)


def validate_run_result(run, folder, result):
    """Same validation for dry-run, commit and aggregation; no mutations."""
    require(all(run.get(key) == result["input"].get(key) for key in ("uc_id", "run_id")), "run identity mismatch")
    version, rubric = method(result["input"])
    require(configured_rubric(run, folder, validate_evidence, result["input"]["baseline"]) == rubric,
            "assessment differs from frozen configuration rubric")
    destination = folder / "flow-accuracy" / result["assessment_id"]
    json_path = destination.with_name(destination.name + ".json")
    md_path = destination.with_name(destination.name + ".md")
    if json_path.exists():
        require(read_json(json_path) == result, "assessment artifact is immutable")
    if md_path.exists():
        require(md_path.read_text(encoding="utf-8") == markdown(result), "assessment report is immutable")
    block = run.get("flow_accuracy")
    history = []
    if block is not None:
        require(method(block) == (version, rubric), "initial/final flow rubric changed")
        history = block.get("assessments")
        require(isinstance(history, list), "invalid flow history")
    previous = next((r for r in history if r.get("assessment_id") == result["assessment_id"]), None)
    if previous is not None:
        require(previous == result, "assessment ID is immutable")
        return
    require(result["stage"] != "initial" or not history, "initial assessment must be first")
    require(result["stage"] != "final" or (history and history[0].get("stage") == "initial"),
            "final assessment requires an immutable initial assessment")
    if history:
        require(history[0]["input"]["baseline"] == result["input"]["baseline"], "flow baseline changed")
        require(all(method(r["input"]) == (version, rubric) for r in history), "mixed method history")
        followups = block.get("followups", [])
        previous_end = max([epoch(r["input"]["captured_at"]) for r in history] +
                           [epoch(r["recorded_at"]) for r in followups
                            if r["assessment_id"] in {a["assessment_id"] for a in history}])
        old_ids = {o["observation_id"] for r in history for o in r["input"]["observations"]}
        old_ids.update(o["observation_id"] for r in followups if r["mode"] == "llm_measurement"
                       for o in r["runtime_result"]["input"].get("observations", []))
        require(epoch(result["input"]["captured_at"]) > previous_end, "new final assessment must follow prior evidence capture")
        for observation in result["input"]["observations"]:
            require(observation["observation_id"] not in old_ids and epoch(observation["started_at"]) > previous_end,
                    "new final assessments require fresh observations")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-json", required=True, type=Path)
    parser.add_argument("--assessment", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path, run, folder = context(args.run_json)
    require(path.is_relative_to(ROOT / "docs/04-experiments"), "flow scores require canonical experiment JSON")
    result = calculate(read_json(args.assessment))
    validate_run_result(run, folder, result)
    if not args.dry_run:
        with run_lock(folder):
            run = read_json(path)
            validate_run_result(run, folder, result)
            version, rubric = method(result["input"])
            destination = folder / "flow-accuracy" / result["assessment_id"]
            json_path = destination.with_name(destination.name + ".json")
            md_path = destination.with_name(destination.name + ".md")
            if run.get("flow_accuracy") is None:
                run["flow_accuracy"] = {"schema_version": version, "rubric_id": rubric, "assessments": []}
            block = run["flow_accuracy"]
            require(method(block) == (version, rubric), "unknown flow schema")
            history = block.get("assessments")
            require(isinstance(history, list), "invalid flow history")
            previous = next((row for row in history if row.get("assessment_id") == result["assessment_id"]), None)
            if previous:
                require(previous == result, "assessment ID is immutable")
            else:
                require(result["stage"] != "initial" or not history, "initial assessment must be first")
                require(result["stage"] != "final" or (history and history[0].get("stage") == "initial"),
                        "final assessment requires an immutable initial assessment")
                if history:
                    require(history[0]["input"]["baseline"] == result["input"]["baseline"], "flow baseline changed")
                history.append(result)
                block["current_assessment_id"] = result["assessment_id"]
                run["flow_accuracy_percent"] = result["flow_accuracy_percent"]
                run["flow_error_percent"] = result["flow_error_percent"]
                run["flow_accuracy_status"] = result["status"]
            summary = refresh_summary(run, folder)
            atomic_write(path, run)
            if not json_path.exists():
                atomic_write(json_path, result)
            if not md_path.exists():
                atomic_write(md_path, markdown(result), raw=True)
            refresh_report(path, run)
    version, rubric = method(result["input"])
    if args.dry_run:
        import copy
        preview = copy.deepcopy(run)
        block = preview.setdefault("flow_accuracy", None)
        if block is None:
            block = preview["flow_accuracy"] = {"schema_version": version, "rubric_id": rubric, "assessments": []}
        if not any(a["assessment_id"] == result["assessment_id"] for a in block["assessments"]):
            block["assessments"].append(result)
            block["current_assessment_id"] = result["assessment_id"]
        summary = refresh_summary(preview, folder)
    print(json.dumps({"schema_version": version, "rubric_id": rubric,
                      **{key: value for key, value in result.items() if key != "input"},
                      "current_summary": summary},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"flow assessment error: {exc}")
