#!/usr/bin/env python3
"""Capture a system instant and persist a UC-bound work segment, never backfill time."""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from metrics_contract import (CORE, AUX, TIMING_PROTOCOL, context, journal, require, run_lock, save_journal)
from measure_uc_tokens import analyze_session, classified_phase, find_turn


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-json", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--turn-id", required=True)
    parser.add_argument("--phase", choices=CORE + AUX, required=True)
    parser.add_argument("--event", choices=("start", "end", "abandon"), required=True)
    parser.add_argument("--segment-id", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--repair-id", help="Required for every repair execution endpoint")
    parser.add_argument("--reason", help="Required for abandoning a missing endpoint after interruption")
    args = parser.parse_args()
    _, run, folder = context(args.run_json)
    if args.event == "start" and args.phase in ("prompt_generation", "source_generation"):
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "gen-coding-prompt/scripts"))
        from preflight_configuration import preflight
        preflight(run["uc_id"], run_id=run["run_id"], run_json=args.run_json,
                  stage="prompt" if args.phase == "prompt_generation" else "source")
    require(re.fullmatch(r"sha256:[0-9a-fA-F]{64}", args.source_revision), "source revision needs full SHA-256")
    session = analyze_session(args.session)
    turn = find_turn(session, args.turn_id)
    require(not turn["completed"] and turn == session["turns"][-1], "capture only in the current active turn")
    with run_lock(folder):
        state = journal(run, folder)
        require(state.get("timing_protocol") == TIMING_PROTOCOL,
                "unsupported timing protocol")
        require(args.phase != "repair" or bool(args.repair_id), "repair timing requires --repair-id")
        require(state["workflow_status"] == "open", "workflow is finalized")
        require(state["session_id"] in (None, session["session_id"]), "session identity mismatch")
        state["session_id"] = session["session_id"]
        require(args.turn_id not in {o["measurement_turn_id"] for o in state["observations"]},
                "measurement turn cannot capture workflow work")
        if args.event == "abandon":
            matches = [s for s in state["segments"] if s["start"]["segment_id"] == args.segment_id]
            require(len(matches) == 1 and "end" not in matches[0] and args.reason,
                    "abandon requires one unfinished segment and an explicit reason")
            original = find_turn(session, matches[0]["start"]["turn_id"])
            require(original["completed"] and original["turn_id"] != args.turn_id,
                    "abandon is only for an earlier terminal turn with a missing endpoint")
            require(matches[0]["start"]["phase"] == args.phase, "abandon phase mismatch")
            require(matches[0]["start"].get("repair_id") == args.repair_id, "abandon repair ID mismatch")
            matches[0]["timing_unavailable_reason"] = args.reason
            matches[0]["abandoned_in_turn_id"] = args.turn_id
            save_journal(folder, state)
            print("Missing endpoint recorded; original time remains unavailable (no end timestamp invented).")
            return
        phase_entry = state["phases"].get(args.phase)
        if args.phase in CORE and not phase_entry:
            require(args.event == "start", "phase must start before ending")
            require(not any(p["status"] == "open" for p in state["phases"].values()), "close previous phase first")
            require(not any(s["start"]["turn_id"] == args.turn_id and s["start"]["phase"] in CORE
                            and s["start"]["phase"] != args.phase for s in state["segments"]),
                    "do not execute different core phases in one turn")
            prior = CORE[:CORE.index(args.phase)]
            require(all(state["phases"].get(p, {}).get("status") == "closed" for p in prior),
                    "preceding phase must be measured and closed first")
            if args.phase in ("source_generation", "repair"):
                activation = run.get("experiment_configuration", {}).get("run_activation")
                from metrics_contract import ROOT, read_json
                if activation and (ROOT / activation).is_file():
                    receipt = read_json(ROOT / activation)
                    require(all(receipt.get(k) == run[k] for k in ("uc_id", "run_id")), "run activation mismatch")
                    require(receipt.get("status") == "Confirmed" and receipt.get("artifact_type") == "run-activation",
                            "existing run activation must be Confirmed")
            if args.phase == "repair":
                require(run.get("business_rules", {}).get("initial", {}).get("requirements"),
                        "repair requires persisted first-pass BR assessment")
                sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "advance-experiment-gate/scripts"))
                from record_gate import validate_repair_authorization
                approval = validate_repair_authorization(run)
                require(run.get("gates", {}).get("current") == "repair", "repair gate must be current")
                approval_turn = find_turn(session, approval["turn_id"])
                source_boundary = find_turn(session, state["phases"]["source_generation"]["measurement_turn_id"])
                require(source_boundary["turn_number"] < approval_turn["turn_number"] <= turn["turn_number"],
                        "repair decision must follow source measurement")
                require(approval_turn["message"].strip() and approval["turn_id"] not in
                        {o["measurement_turn_id"] for o in state["observations"]},
                        "repair decision must belong to a work turn, never a measurement turn")
            state["phases"][args.phase] = {"status": "open", "first_turn_id": args.turn_id}
        expected = classified_phase(state, turn, session)
        require(args.phase in AUX or args.phase == expected,
                "timestamp phase conflicts with open/closed phase boundaries")
        segments = state["segments"]
        matches = [s for s in segments if s["start"]["segment_id"] == args.segment_id]
        now = datetime.now().astimezone()
        value = {"at": now.isoformat(timespec="milliseconds"), "epoch_ms": round(now.timestamp() * 1000),
                 "timing_protocol": TIMING_PROTOCOL,
                 "uc_id": run["uc_id"], "run_id": run["run_id"], "session_id": session["session_id"],
                 "turn_id": args.turn_id, "phase": args.phase, "event": args.event,
                 "segment_id": args.segment_id, "source_revision": args.source_revision}
        if args.phase == "repair":
            value["repair_id"] = args.repair_id
        if args.event == "start":
            require(not matches, "segment ID already exists; timestamps are immutable")
            require(all("end" in s or s.get("timing_unavailable_reason") for s in segments),
                    "end previous work segment or record its unavailable endpoint before starting another")
            segments.append({"start": value})
        else:
            require(len(matches) == 1 and "end" not in matches[0], "missing/already ended segment")
            require(all(matches[0]["start"][k] == value[k] for k in ("turn_id", "phase", "session_id")),
                    "end must match start identity in the same turn")
            require(matches[0]["start"].get("repair_id") == value.get("repair_id"), "repair ID differs from start")
            matches[0]["end"] = value
        save_journal(folder, state)
        import json
        print(json.dumps(value, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        sys.exit(f"timestamp error: {exc}")
