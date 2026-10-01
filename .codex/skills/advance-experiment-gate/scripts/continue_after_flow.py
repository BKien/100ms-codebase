#!/usr/bin/env python3
"""Record the policy decision after a saved flow follow-up; never edit source."""

import argparse
import copy
import json

from record_gate import (ROOT, atomic_write, automatic_context, context, prepare_transition,
                         read_json, require, run_lock, validate_repair_authorization)
from flow_summary import refresh_report


def prepare(run, folder, followup_id, turn_id, source_revision):
    updated = copy.deepcopy(run)
    gate = (run.get("gates") or {}).get("current")
    prior = next((r for r in (run.get("gates") or {}).get("history", [])
                  if r.get("gate") == "repair_decision"), None)
    if prior or gate != "repair_decision":
        # A replay or a late researcher reply must never open another repair cycle.
        if gate == "repair" and prior and prior.get("outcome") == "authorized":
            validate_repair_authorization(run)
        return updated, {"action": "no_transition", "current_gate": gate,
                         "reason": "Decision already recorded or run is outside Repair Decision; retain existing scope."}
    outcome, automatic = automatic_context(run, folder, followup_id, source_revision)
    if outcome is None:
        return updated, {"action": "measurement_pending", "current_gate": gate,
                         "reason": "Measurement remains incomplete; save conclusive results for pending flows before repair."}
    if outcome == "authorized":
        return updated, {"action": "await_repair_request", "current_gate": gate,
                         "reason": "Researcher results saved. Invoke $bug-fixing-sub-prompt to authorize and begin repair without another confirmation."}
    reason = "No evidenced defects remain after the saved flow follow-up; repair is unnecessary." if outcome == "skipped" else None
    receipt = prepare_transition(updated, folder, "repair_decision", outcome, turn_id, reason, automatic)
    return updated, {"action": "final_metrics",
                     "current_gate": updated["gates"]["current"], "receipt": receipt}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-json", required=True)
    parser.add_argument("--followup-id", required=True)
    parser.add_argument("--turn-id", required=True, help="Actual work turn, not a fabricated confirmation")
    parser.add_argument("--source-revision", required=True, help="Current source hash verified by the caller")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path, run, folder = context(args.run_json)
    require(path.is_relative_to(ROOT / "docs/04-experiments"), "continuation requires canonical experiment JSON")
    if args.dry_run:
        _, result = prepare(run, folder, args.followup_id, args.turn_id, args.source_revision)
    else:
        with run_lock(folder):
            run = read_json(path)
            updated, result = prepare(run, folder, args.followup_id, args.turn_id, args.source_revision)
            if updated != run:
                atomic_write(path, updated)
            refresh_report(path, updated)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"flow continuation error: {exc}")
