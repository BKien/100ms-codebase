#!/usr/bin/env python3
"""Extract and persist post-turn UC telemetry from cumulative usage counters."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from metrics_contract import (CORE, AUX, USAGE, METHOD, TIMING_PROTOCOL, aggregate, execution_phase_aggregate,
                              execution_workflow_aggregate, repair_timing, token_breakdown, atomic_write, context,
                              digest, duration, epoch, journal, metrics_markdown, read_json,
                              require, run_lock, save_journal, usage, validate_core_token_phase, validate_metrics,
                              wall_clock_seconds)

START = {"turn_started", "task_started"}
END = {"turn_complete", "turn_completed", "task_complete", "task_completed"}
ABORT = {"turn_aborted", "task_aborted"}


def analyze_session(path):
    raw = Path(path).read_bytes()
    lines = raw.splitlines(keepends=True)
    turns, current, previous, session_id = [], None, None, None
    offset = 0
    diagnostics = {"token_updates": 0, "duplicate_updates": 0, "counter_resets": 0}
    for index, line in enumerate(lines):
        offset += len(line)
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            # The only tolerated partial record is the actively appended last line.
            require(index == len(lines) - 1 and not line.endswith(b"\n"), "malformed JSONL record")
            break
        top, payload = record.get("type"), record.get("payload") or {}
        kind, at = payload.get("type"), record.get("timestamp")
        if top == "session_meta":
            session_id = payload.get("id") or session_id
        if top == "event_msg" and kind in START:
            if current:
                turns.append(current)  # Missing completion is never inferred from next start.
            current = {"turn_id": payload.get("turn_id"), "turn_number": len(turns) + 1,
                       "started_at": at, "ended_at": None, "completed": False,
                       "message": "", "model": None, "tokens": None,
                       "turn_context_seen": False, "user_message_seen": False,
                       "usage_updates": 0, "tool_call_count": 0, "call_ids": set(),
                       "prefix_bytes": None, "prefix_sha256": None}
        elif top == "turn_context" and current:
            current["turn_context_seen"] = True
            current["turn_id"] = current["turn_id"] or payload.get("turn_id")
            current["model"] = payload.get("model") or current["model"]
        elif top == "event_msg" and kind == "user_message" and current:
            message = payload.get("message")
            if isinstance(message, str):
                current["message"] = message.strip()
                current["user_message_seen"] = True
        elif top == "response_item" and current:
            # Bootstrap context precedes turn_context; the first user response
            # after it is the request, followed by optional injected skill text.
            if payload.get("role") == "user" and current["turn_context_seen"] and not current["user_message_seen"]:
                current["message"] = "\n".join(x.get("text", "") for x in payload.get("content", [])
                                                 if isinstance(x, dict) and x.get("type") in ("input_text", "text"))
                current["user_message_seen"] = bool(current["message"].strip())
            if isinstance(kind, str) and kind.endswith("_call"):
                call_id = payload.get("call_id") or payload.get("id")
                if not call_id or call_id not in current["call_ids"]:
                    current["tool_call_count"] += 1
                    if call_id:
                        current["call_ids"].add(call_id)
        elif top == "event_msg" and kind in END | ABORT and current:
            require(not payload.get("turn_id") or payload["turn_id"] == current["turn_id"],
                    "completion turn identity mismatch")
            current.update(ended_at=at, completed=True, terminal_event=kind,
                           prefix_bytes=offset, prefix_sha256=digest(raw[:offset]))
            turns.append(current)
            current = None
        if top != "event_msg" or kind != "token_count":
            continue
        info = payload.get("info") or {}
        if not isinstance(info.get("total_token_usage"), dict):
            continue
        counters = usage(info["total_token_usage"])
        if counters == previous:
            diagnostics["duplicate_updates"] += 1
            continue
        backwards = previous is not None and any(
            counters[k] is not None and previous[k] is not None and counters[k] < previous[k] for k in USAGE)
        if backwards:
            diagnostics["counter_resets"] += 1
            delta = usage(info.get("last_token_usage"))
        elif previous is None:
            delta = counters.copy()
            if current and isinstance(info.get("last_token_usage"), dict):
                first_usage = usage(info["last_token_usage"])
                require(all(counters[k] == first_usage[k] for k in ("input_tokens", "output_tokens", "total_tokens")),
                        "first cumulative event contains prior usage without a baseline; supply complete rollout")
        else:
            delta = {k: None if counters[k] is None or previous[k] is None else counters[k] - previous[k]
                     for k in USAGE}
        previous = counters
        diagnostics["token_updates"] += 1
        if current:
            old = current["tokens"]
            current["tokens"] = delta if old is None else {
                k: None if old[k] is None or delta[k] is None else old[k] + delta[k] for k in USAGE}
            current["usage_updates"] += 1
    if current:
        turns.append(current)
    require(session_id, "session_meta.id required; do not infer identity from latest file")
    require(all(t["turn_id"] for t in turns), "explicit turn IDs required")
    require(len({t["turn_id"] for t in turns}) == len(turns), "duplicate turn IDs")
    return {"session_id": session_id, "file_name": Path(path).name,
            "sha256": digest(raw), "turns": turns, "diagnostics": diagnostics}


def public_turn(turn):
    return {k: v for k, v in turn.items() if k not in (
        "message", "call_ids", "usage_updates", "turn_context_seen", "user_message_seen")} | {
        "message_sha256": digest(turn["message"].encode("utf-8"))}


def find_turn(session, turn_id):
    values = [t for t in session["turns"] if t["turn_id"] == turn_id]
    require(len(values) == 1, f"turn not uniquely found: {turn_id}")
    return values[0]


def classified_phase(state, turn, session):
    """Return the live timing/control bucket, never a semantic token label."""
    number = turn["turn_number"]
    for phase, value in state["phases"].items():
        if value["status"] == "skipped":
            continue
        start = find_turn(session, value["first_turn_id"])["turn_number"]
        end = (find_turn(session, value["measurement_turn_id"])["turn_number"]
               if value.get("measurement_turn_id") else float("inf"))
        if start <= number < end:
            return phase
    return None


def close_repair_and_finalize(state, run, rows, selection, measurement_turn_id):
    """Close/skip Repair and finalize the ledger as one validated operation."""
    require(all(state["phases"].get(p, {}).get("status") == "closed" for p in CORE[:2]),
            "prompt/source phases must be closed")
    require(run.get("run_status") in ("complete", "blocked", "stopped", "repair_declined"),
            "workflow requires an explicit terminal run status")
    repair = state["phases"].get("repair")
    if not repair:
        skip_reason = run.get("repair_skip_reason") or selection.get("repair_skip_reason")
        require(not run.get("repairs") and bool(skip_reason)
                and run.get("gates", {}).get("current") == "final_metrics",
                "unperformed repair needs the persisted all-passing/no-repair decision")
        selected_reason = selection.get("repair_skip_reason")
        require(not selected_reason or selected_reason == skip_reason,
                "selection repair-skip reason conflicts with the canonical decision")
        state["phases"]["repair"] = {"status": "skipped", "reason": skip_reason}
    elif repair["status"] == "open":
        require(any(row["timing_phase"] == "repair" for row in rows),
                "no evidence for closing repair phase")
        require(all(segment.get("end") or segment.get("timing_unavailable_reason")
                    for segment in state["segments"] if segment["start"]["phase"] == "repair"),
                "end captured repair interval before finalizing")
        repair.update(status="closed", measurement_turn_id=measurement_turn_id)
    else:
        require(repair["status"] in {"closed", "skipped"},
                "repair phase must be open, closed or skipped")
    state["workflow_status"] = "finalized"


def prepare_finalize_run(run, folder, measurement_turn_id):
    """Validate internal Repair-close then Final receipts before canonical commit."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "advance-experiment-gate/scripts"))
    from record_command import prepare
    if run.get("gates", {}).get("current") == "repair":
        run, _ = prepare(run, folder, "repair-close", measurement_turn_id)
    run, _ = prepare(run, folder, "finalize", measurement_turn_id)
    return run


def measure(args):
    path, run, folder = context(args.run_json)
    selection = read_json(args.selection)
    require(all(selection.get(k) == run[k] for k in ("uc_id", "run_id")), "selection UC/run mismatch")
    session = analyze_session(selection["session_path"])
    measurement = find_turn(session, args.measurement_turn_id)
    require(measurement == session["turns"][-1] and not measurement["completed"],
            "measurement ID must identify the current active turn")
    with run_lock(folder):
        state = journal(run, folder)
        require(state.get("timing_protocol") == TIMING_PROTOCOL,
                "unsupported timing protocol")
        require(state["session_id"] in (None, session["session_id"]), "one session per UC/run required")
        state["session_id"] = session["session_id"]
        ids = [s["turn_id"] for s in selection["turns"]]
        require(ids and len(set(ids)) == len(ids), "selection is empty or contains duplicates")
        exclusions = selection.get("excluded_turns", [])
        excluded_ids = [e["turn_id"] for e in exclusions]
        require(len(set(excluded_ids)) == len(excluded_ids) and not set(ids) & set(excluded_ids),
                "duplicate or selected exclusion")
        selected = [find_turn(session, i) for i in ids]
        require([t["turn_number"] for t in selected] == sorted(t["turn_number"] for t in selected),
                "selected turns must be in chronological order")
        require(selected[-1]["turn_number"] < measurement["turn_number"],
                "cannot measure current/future turn")
        expected = {t["turn_id"] for t in session["turns"]
                    if t["turn_number"] < measurement["turn_number"]}
        require(set(ids) | set(excluded_ids) == expected, "every bounded turn needs selection or exclusion reason")
        for item in exclusions:
            require(bool(item.get("reason")), "exclusion needs a reason")
        known_measurements = {o["measurement_turn_id"] for o in state["observations"]}
        require(not known_measurements.intersection(ids), "measurement/report turns must be excluded")
        for anchor, actual in (("start", selected[0]), ("terminal", selected[-1])):
            proof = selection["workflow_evidence"][anchor]
            require(proof["turn_id"] == actual["turn_id"], f"{anchor} evidence points to wrong turn")
            terms = proof.get("required_terms", [])
            require(terms and all(isinstance(t, str) and t.strip() and
                    t.casefold() in actual["message"].casefold() for t in terms), f"{anchor} markers mismatch")
        require(run["uc_id"].casefold() in selected[0]["message"].casefold(), "first workflow message must identify UC")
        old_metrics = run.get("metrics")
        if old_metrics:
            require(old_metrics.get("schema_version") == 3 and old_metrics.get("timing_protocol") == TIMING_PROTOCOL,
                    "unsupported metrics schema or timing protocol")
            require(old_metrics["session"]["session_id"] == session["session_id"], "metrics session mismatch")
            old_ids = [r["turn_id"] for r in old_metrics["turns"]]
            require(ids[:len(old_ids)] == old_ids, "cannot remove/reorder previously measured workflow turns")
        rows = []
        intervals = []
        for selector, turn in zip(selection["turns"], selected):
            require(turn["completed"] and turn["tokens"] is not None, "selected turn needs completion and token telemetry")
            usage(turn["tokens"])
            phase = selector["phase"]
            require(phase in CORE + AUX and bool(selector.get("reason")), "phase and classification reason required")
            expected_phase = classified_phase(state, turn, session)
            # Auxiliary work may occur inside any open core bucket. A core label
            # still cannot amend an already closed bucket or authorize new work.
            require(phase in AUX or phase == expected_phase,
                    f"{turn['turn_id']} core token label is outside its generation window")
            segments = [s for s in state["segments"] if s["start"]["turn_id"] == turn["turn_id"]]
            validate_core_token_phase(phase, segments)
            counted = [s for s in segments if s["start"]["phase"] in CORE]
            timing_phases = {s["start"]["phase"] for s in counted}
            require(len(timing_phases) <= 1, "one core execution phase per turn required")
            timing_phase = next(iter(timing_phases), phase)
            require(timing_phase in AUX or timing_phase == expected_phase,
                    "captured timing bucket conflicts with ledger boundaries")
            missing = selector.get("timing_unavailable_reason")
            excluded_time = not counted and phase in AUX
            if excluded_time:
                seconds = 0
            elif not counted or any("end" not in s for s in counted):
                require(bool(missing), "missing captured endpoint: record timing_unavailable_reason, never backfill")
                seconds = None
            else:
                seconds = round(sum(duration(s) for s in counted), 3)
            for segment in segments:
                require(segment["start"].get("timing_protocol") == TIMING_PROTOCOL,
                        "capture timing protocol mismatch")
                if "end" in segment:
                    duration(segment)
                    a, b = segment["start"]["epoch_ms"], segment["end"]["epoch_ms"]
                    require(epoch(turn["started_at"]) - 1000 <= a <= b <= epoch(turn["ended_at"]) + 1000,
                            "captured interval must lie within its completed turn")
                    intervals.append((a, b))
            row = public_turn(turn) | {"session_id": session["session_id"], "phase": phase,
                                      "timing_phase": timing_phase,
                                      "reason": selector["reason"], "duration_seconds": seconds,
                                      "wall_clock_seconds": wall_clock_seconds(turn),
                                      "timing_unavailable_reason": missing if seconds is None else None,
                                      "timing_exclusion_reason": "Auxiliary work excluded from generation time" if excluded_time else None,
                                      "timing_segments": segments}
            if selector.get("repair_id"):
                require(any(r.get("repair_id") == selector["repair_id"] for r in run.get("repairs", [])),
                        "repair_id must match canonical repair entry")
                row["repair_id"] = selector["repair_id"]
            rows.append(row)
        intervals.sort()
        require(all(a[1] <= b[0] for a, b in zip(intervals, intervals[1:])), "overlapping timing segments would double-count")
        if old_metrics:
            require(rows[:len(old_metrics["turns"])] == old_metrics["turns"],
                    "previously measured evidence changed; closed phase is immutable")
        action = args.command + (":" + args.phase if args.command == "close-phase" else "")
        existing = next((o for o in state["observations"] if o["measurement_turn_id"] == args.measurement_turn_id), None)
        if existing:
            require(existing["action"] == action, "measurement turn already used for another operation")
        else:
            require(state["workflow_status"] == "open", "workflow already finalized")
            if args.command == "close-phase":
                entry = state["phases"].get(args.phase)
                require(entry and entry["status"] == "open", "phase must be open before closing")
                require(any(r["timing_phase"] == args.phase for r in rows), "no evidence for closing phase")
                require(all(s.get("end") or s.get("timing_unavailable_reason")
                            for s in state["segments"] if s["start"]["phase"] == args.phase),
                        "end captured work interval before closing phase")
                entry.update(status="closed", measurement_turn_id=args.measurement_turn_id)
            else:
                close_repair_and_finalize(state, run, rows, selection, args.measurement_turn_id)
        phases = {p: {"status": state["phases"].get(p, {}).get("status", "not_started"), "values": None}
                  for p in CORE}
        repair_ids = [r.get("repair_id") for r in run.get("repairs", [])]
        require(all(isinstance(i, str) and i.strip() for i in repair_ids) and len(set(repair_ids)) == len(repair_ids),
                "each canonical repair needs a unique repair_id")
        repairs = repair_timing(rows, repair_ids)
        for p in CORE:
            if phases[p]["status"] == "closed":
                phases[p]["values"] = execution_phase_aggregate(rows, p, repairs)
            elif phases[p]["status"] == "skipped":
                phases[p]["reason"] = state["phases"][p]["reason"]
                phases[p]["values"] = aggregate([])
        evidence_sha = digest(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode("utf-8"))
        if not existing:
            state["observations"].append({"measurement_turn_id": args.measurement_turn_id,
                "action": action, "last_turn_id": rows[-1]["turn_id"], "evidence_sha256": evidence_sha})
        metrics = {"schema_version": 3, "provenance_class": "observed_post_run", "timing_method": METHOD,
                   "timing_protocol": TIMING_PROTOCOL, "repair_timing": repairs,
                   "token_attribution_method": "semantic_primary_phase_per_turn",
                   "uc_id": run["uc_id"], "run_id": run["run_id"], "status": state["workflow_status"],
                   "measured_at": datetime.now(timezone.utc).isoformat(),
                   "session": {k: session[k] for k in ("session_id", "file_name", "sha256")},
                   "selection_evidence_sha256": evidence_sha,
                   "extractor_sha256": digest(Path(__file__).read_bytes()),
                   "phases": phases, "workflow": execution_workflow_aggregate(rows, phases), "turns": rows,
                   "token_phase_breakdown": token_breakdown(rows),
                   "excluded_turns": exclusions + [{"turn_id": args.measurement_turn_id, "reason": "measurement/report turn"}],
                   "phase_ledger": state}
        validate_metrics(metrics)
        # Finalize pre-validates both internal transitions and commits them with
        # telemetry in one canonical write. Ledger/mirrors remain recoverable.
        run = read_json(path)
        run["metrics_schema_version"] = 3
        run["metrics"] = metrics
        finalize_committed = args.command == "finalize-workflow"
        if finalize_committed:
            run = prepare_finalize_run(run, folder, args.measurement_turn_id)
        atomic_write(path, run)
        atomic_write(folder / "workflow-metrics.json", metrics)
        save_journal(folder, state)
        atomic_write(folder / "workflow-metrics.md", metrics_markdown(metrics), raw=True)
        require(read_json(path)["metrics"] == read_json(folder / "workflow-metrics.json"), "persisted metrics mismatch")
        if run.get("run_status") == "complete":
            report_path = path.with_suffix(".md")
            if run.get("report_artifact"):
                from metrics_contract import ROOT, writable
                report_path = writable(ROOT / run["report_artifact"])
            if report_path.exists():
                import subprocess
                from metrics_contract import ROOT
                renderer = ROOT / ".codex/skills/render-experiment-report/scripts/render_report.py"
                subprocess.run([sys.executable, "-B", str(renderer), str(path), "--output", str(report_path)], check=True)
        print(metrics_markdown(metrics))
    # Non-final telemetry succeeds first; record its command in the same excluded close turn.
    # A failed receipt is recoverable by record_command.py without remeasuring tokens.
    if not finalize_committed:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "advance-experiment-gate/scripts"))
        from record_command import prepare, commit
        action = {"prompt_generation": "prompt-close", "source_generation": "source-close"}[args.phase]
        with run_lock(folder):
            current = read_json(path)
            updated, _ = prepare(current, folder, action, args.measurement_turn_id)
            if updated != current or action == "prompt-close":
                commit(path, updated, folder, action, args.measurement_turn_id)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="Read-only list of explicit turns; never writes final metrics")
    listing.add_argument("--session", type=Path, required=True)
    for command in ("close-phase", "finalize-workflow"):
        sub = commands.add_parser(command)
        sub.add_argument("--run-json", type=Path, required=True)
        sub.add_argument("--selection", type=Path, required=True)
        sub.add_argument("--measurement-turn-id", required=True)
        if command == "close-phase":
            sub.add_argument("--phase", choices=("prompt_generation", "source_generation"), required=True)
    args = parser.parse_args()
    if args.command == "list":
        session = analyze_session(args.session)
        session["turns"] = [public_turn(t) for t in session["turns"]]
        print(json.dumps(session, ensure_ascii=False, indent=2))
    else:
        measure(args)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        sys.exit(f"measurement error: {exc}")
