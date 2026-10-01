#!/usr/bin/env python3
"""Persist flow progress or researcher/LLM results without altering source or telemetry."""

import argparse
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "measure-uc-workflow/scripts"))
from metrics_contract import ROOT, atomic_write, context, read_json, require, run_lock
from flow_summary import RESULT_POLICY, current_assessment, fingerprint, refresh_report, refresh_summary


def prepare(run, folder, payload=None):
    # Audit validation is read-only here, including the prior immutable assessments.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "audit-generation-metrics/scripts"))
    from calculate_metrics import validate_flow
    from score_flow_accuracy import calculate
    validate_flow(run, folder)
    updated = copy.deepcopy(run)
    updated["flow_accuracy"]["selection_policy"] = RESULT_POLICY
    if payload is not None:
        record = copy.deepcopy(payload)
        if record.get("mode") == "llm_measurement":
            record["runtime_result"] = calculate(record.pop("runtime_assessment"))
        history = updated["flow_accuracy"].setdefault("followups", [])
        previous = next((r for r in history if r.get("followup_id") == record.get("followup_id")), None)
        require(previous is None or previous == record, "follow-up ID is immutable")
        parent = next((a for a in updated["flow_accuracy"]["assessments"]
                       if a["assessment_id"] == record.get("assessment_id")), None)
        require(parent is not None and record.get("assessment_sha256") == fingerprint(parent),
                "follow-up must identify its immutable evidence assessment")
        if previous is None and record.get("mode") == "llm_measurement":
            require(parent == current_assessment(updated), "LLM observation requires the current source assessment")
            recorded_source = (run.get("business_rules") or {}).get("source_revision")
            require(recorded_source is None or recorded_source == parent["input"]["source_revision"],
                    "current source record differs from the flow assessment; do not mix runtime revisions")
        if previous is None:
            history.append(record)
    summary = refresh_summary(updated, folder)
    validate_flow(updated, folder)
    return updated, summary


def persist(path, run, folder, summary):
    # Follow-ups are validated append-only records in canonical JSON.
    atomic_write(path, run)
    refresh_report(path, run)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-json", required=True, type=Path)
    parser.add_argument("--input", help="Follow-up JSON path, or '-' for stdin without a payload file; omit to refresh results")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path, run, folder = context(args.run_json)
    require(path.is_relative_to(ROOT / "docs/04-experiments"),
            "flow follow-up writes only canonical experiment JSON under docs/04-experiments")
    reserved = (folder / "flow-accuracy").resolve()
    require(not path.is_relative_to(reserved), "canonical JSON cannot be a flow evidence artifact")
    payload = json.load(sys.stdin) if args.input == "-" else (read_json(Path(args.input)) if args.input else None)
    if args.dry_run:
        _, summary = prepare(run, folder, payload)
    else:
        with run_lock(folder):
            updated, summary = prepare(read_json(path), folder, payload)
            persist(path, updated, folder, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"flow follow-up error: {exc}")
