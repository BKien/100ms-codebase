"""Shared, deterministic contract for observed UC metrics (standard library only)."""

import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

CORE = ("prompt_generation", "source_generation", "repair")
AUX = ("configuration_and_approval", "dataset_resolution", "audit",
       "runtime_verification", "finalization", "uc_setup")
USAGE = ("input_tokens", "cached_input_tokens", "output_tokens",
         "reasoning_output_tokens", "total_tokens")
METHOD = "system_timestamp_delta"
TIMING_PROTOCOL = "generation_execution_with_repair_audit_v2"
ROOT = Path(__file__).resolve().parents[4]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def writable(path):
    path = Path(path).resolve()
    require(path.is_relative_to(ROOT), "output must stay inside Business repository")
    relative = path.relative_to(ROOT)
    require(not relative.parts or not relative.parts[0].lower().endswith("-master"),
            "external reference projects are read-only")
    return path


def validate_canonical_path(path, run):
    path = writable(path)
    expected_parent = writable(ROOT / "docs/04-experiments" / run["uc_id"])
    expected_name = f"canonical-run-{run['run_id']}.json"
    require(path.parent == expected_parent and path.name == expected_name,
            f"canonical run must be stored at docs/04-experiments/{run['uc_id']}/{expected_name}")
    return path


def atomic_write(path, value, raw=False):
    path = writable(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = value if raw else json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    fd, temp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def context(run_path):
    path = writable(run_path)
    run = read_json(path)
    for key in ("uc_id", "run_id"):
        value = run.get(key)
        require(isinstance(value, str) and value and
                all(c.isalnum() or c in "-_." for c in value) and value not in (".", ".."),
                f"invalid {key}")
    validate_canonical_path(path, run)
    folder = writable(ROOT / "docs/02-construction/implementation" /
                      run["uc_id"] / "runs" / run["run_id"])
    return path, run, folder


@contextmanager
def run_lock(folder):
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ".metrics.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ValueError("metrics writer already active; inspect lock before retrying") from exc
    try:
        os.close(fd)
        yield
    finally:
        path.unlink()


def journal(run, folder):
    path = folder / "phase-ledger.json"
    value = read_json(path) if path.exists() else {
        "schema_version": 1, "uc_id": run["uc_id"], "run_id": run["run_id"],
        "session_id": None, "phases": {}, "segments": [], "observations": [],
        "workflow_status": "open", "timing_protocol": TIMING_PROTOCOL}
    require(all(value[k] == run[k] for k in ("uc_id", "run_id")), "ledger identity mismatch")
    committed = (run.get("metrics") or {}).get("phase_ledger")
    if committed and len(committed["observations"]) > len(value["observations"]):
        # Recovery after canonical commit succeeded but a mirror write was interrupted.
        value = json.loads(json.dumps(committed))
    return value


def save_journal(folder, value):
    atomic_write(folder / "phase-ledger.json", value)
    lines = ["# UC phase ledger", "", f"UC: `{value['uc_id']}`; run: `{value['run_id']}`",
             "", "Machine authority: phase-ledger.json. Each turn belongs to one phase.",
             "", "| Phase | Status | First turn | Measurement boundary (excluded) |",
             "|---|---|---|---|"]
    for phase in CORE:
        item = value["phases"].get(phase, {})
        lines.append(f"| {phase} | {item.get('status', 'not_started')} | "
                     f"{item.get('first_turn_id', '')} | {item.get('measurement_turn_id', '')} |")
    lines += ["", f"Workflow: {value['workflow_status']}", "",
              "## Measurements", "", "All measurement turns are excluded from phase and workflow metrics.", ""]
    for item in value["observations"]:
        lines.append(f"- `{item['measurement_turn_id']}`: {item['action']}; last selected turn "
                     f"`{item['last_turn_id']}`; evidence `{item['evidence_sha256']}`")
    atomic_write(folder / "phase-ledger.md", "\n".join(lines) + "\n", raw=True)


def epoch(at):
    require(isinstance(at, str), "missing ISO timestamp")
    parsed = datetime.fromisoformat(at.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "timestamp requires timezone")
    return round(parsed.timestamp() * 1000)


def endpoint(value):
    ms = value.get("epoch_ms")
    require(type(ms) is int and abs(epoch(value.get("at")) - ms) <= 1000,
            "ISO and epoch must describe the same instant within one second")
    return ms


def wall_clock_seconds(turn):
    """Elapsed seconds within one selected rollout turn, including approval waits."""
    require(turn.get("completed"), "wall-clock requires a completed turn")
    start, end = epoch(turn.get("started_at")), epoch(turn.get("ended_at"))
    require(end >= start, "negative turn wall-clock duration")
    return round((end - start) / 1000, 3)


def duration(segment):
    start, end = segment["start"], segment["end"]
    for key in ("uc_id", "run_id", "session_id", "turn_id", "phase", "segment_id"):
        require(start.get(key) == end.get(key), f"timestamp {key} mismatch")
    require(start.get("repair_id") == end.get("repair_id"), "timestamp repair identity mismatch")
    require(start["event"] == "start" and end["event"] == "end", "invalid timestamp events")
    a, b = endpoint(start), endpoint(end)
    require(b >= a, "negative duration")
    return round((b - a) / 1000, 3)


def usage(raw):
    require(isinstance(raw, dict), "missing token counters")
    result = {}
    for key in USAGE:
        value = raw.get(key)
        require(value is None or (type(value) is int and value >= 0), f"invalid {key}")
        result[key] = value
    require(all(result[k] is not None for k in ("input_tokens", "output_tokens", "total_tokens")),
            "input/output/total token counters required")
    require(result["total_tokens"] == result["input_tokens"] + result["output_tokens"],
            "total_tokens must equal input_tokens + output_tokens")
    for child, parent in (("cached_input_tokens", "input_tokens"),
                          ("reasoning_output_tokens", "output_tokens")):
        require(result[child] is None or result[child] <= result[parent], f"{child} exceeds {parent}")
    return result


def aggregate(rows):
    result = {key: (None if any(r["tokens"][key] is None for r in rows)
                    else sum(r["tokens"][key] for r in rows)) for key in USAGE}
    reasons = {key: "Counter unavailable in at least one selected turn"
               for key in USAGE if result[key] is None}
    times = [r["duration_seconds"] for r in rows]
    return {"tokens": result, "token_unavailable_reasons": reasons,
            "duration_seconds": None if any(t is None for t in times) else round(sum(times), 3),
            "wall_clock_seconds": round(sum(r["wall_clock_seconds"] for r in rows), 3),
            "timing_unavailable_reason": "Missing captured endpoints; see turns" if None in times else None,
            "workflow_turn_count": len(rows),
            "tool_call_count": sum(r["tool_call_count"] for r in rows),
            "model_call_count": None,
            "model_call_count_unavailable_reason": "Rollout usage updates are not proven model request events"}


def phase_aggregate(rows, phase):
    """Token/count membership is semantic; time retains its captured bucket."""
    result = aggregate([r for r in rows if r["phase"] == phase])
    timed = aggregate([r for r in rows if r["timing_phase"] == phase])
    for key in ("duration_seconds", "timing_unavailable_reason"):
        result[key] = timed[key]
    return result


def token_breakdown(rows):
    result = {}
    for phase in sorted({r["phase"] for r in rows}):
        values = aggregate([r for r in rows if r["phase"] == phase])
        result[phase] = {k: values[k] for k in (
            "tokens", "token_unavailable_reasons", "wall_clock_seconds", "workflow_turn_count", "tool_call_count")}
    return result


def repair_timing(rows, repair_ids):
    result = {}
    for repair_id in repair_ids:
        segments = [s for r in rows for s in r.get("timing_segments", [])
                    if s["start"]["phase"] == "repair" and s["start"].get("repair_id") == repair_id]
        missing = not segments or any("end" not in s for s in segments)
        result[repair_id] = {
            "duration_seconds": None if missing else round(sum(duration(s) for s in segments), 3),
            "timing_unavailable_reason": "Missing repair execution endpoints" if missing else None,
            "segment_ids": [s["start"]["segment_id"] for s in segments]}
    return result


def execution_phase_aggregate(rows, phase, repairs):
    result = phase_aggregate(rows, phase)
    if phase == "repair":
        times = [v["duration_seconds"] for v in repairs.values()]
        missing = any(v is None for v in times) or result["duration_seconds"] is None
        result["duration_seconds"] = None if missing else round(sum(times), 3)
        result["timing_unavailable_reason"] = "Missing repair execution endpoints" if missing else None
    return result


def execution_workflow_aggregate(rows, phases):
    result = aggregate(rows)
    times = [p["values"]["duration_seconds"] if p.get("values") is not None else None for p in phases.values()]
    missing = any(t is None for t in times)
    result["duration_seconds"] = None if missing else round(sum(times), 3)
    result["timing_unavailable_reason"] = "Generation phase timing pending or unavailable; see phases" if missing else None
    return result


def validate_core_token_phase(phase, segments):
    """A captured core execution anchors the whole turn, including its child audit."""
    core_phases = {s["start"]["phase"] for s in segments if s["start"]["phase"] in CORE}
    require(len(core_phases) <= 1, "one core execution phase per turn required")
    require(not core_phases or phase in core_phases,
            "token label must match captured core execution phase; integrated repair audit belongs to repair")


def validate_metrics(metrics):
    require(metrics.get("schema_version") == 3, "unsupported metrics schema")
    protocol = metrics.get("timing_protocol")
    require(protocol == TIMING_PROTOCOL, "unsupported timing protocol")
    require(metrics.get("token_attribution_method") == "semantic_primary_phase_per_turn",
            "unsupported token attribution method")
    require(metrics.get("timing_method") == METHOD, "unsupported timing method")
    rows = metrics.get("turns", [])
    require(len({(r["session_id"], r["turn_id"]) for r in rows}) == len(rows), "duplicate turn")
    for row in rows:
        usage(row["tokens"])
        require(row["phase"] in CORE + AUX and row["completed"], "invalid selected turn")
        require(bool(row.get("reason")), "turn classification needs a reason")
        require(row.get("timing_phase") in CORE + AUX, "valid timing bucket required")
        require(type(row.get("tool_call_count")) is int and row["tool_call_count"] >= 0, "invalid tool-call count")
        require(row["duration_seconds"] is None or row["duration_seconds"] >= 0, "negative time")
        require(type(row.get("wall_clock_seconds")) in (int, float)
                and row["wall_clock_seconds"] == wall_clock_seconds(row),
                "turn wall-clock differs from rollout boundaries")
        segments = row.get("timing_segments", [])
        validate_core_token_phase(row["phase"], segments)
        timed_segments = [s for s in segments if s["start"]["phase"] in CORE]
        if not timed_segments and row["phase"] in AUX:
            require(row["duration_seconds"] == 0 and bool(row.get("timing_exclusion_reason")),
                    "auxiliary-only work must have zero counted generation seconds and an exclusion reason")
        elif row["duration_seconds"] is None:
            require(bool(row.get("timing_unavailable_reason")), "missing time needs a reason")
        else:
            require(bool(timed_segments), "observed duration needs captured segments")
            require(round(sum(duration(s) for s in timed_segments), 3) == row["duration_seconds"],
                    "duration differs from captured endpoints")
        for segment in segments:
            require(segment["start"].get("timing_protocol") == protocol,
                    "timestamps must retain their recorded timing protocol")
            if "end" in segment:
                require(segment["end"].get("timing_protocol") == protocol, "end timing protocol mismatch")
                duration(segment)
            if segment["start"]["phase"] == "repair":
                require(segment["start"].get("repair_id") in metrics.get("repair_timing", {}),
                        "repair segment missing canonical repair identity")
        for segment in segments:
            require(all(segment["start"].get(k) == metrics[k] for k in ("uc_id", "run_id")),
                    "segment UC/run mismatch")
            require(all(segment["start"].get(k) == row[k] for k in ("turn_id", "session_id")),
                    "segment turn identity mismatch")
            require((segment["start"]["phase"] in AUX) or
                    segment["start"]["phase"] == row["timing_phase"],
                    "segment timing bucket mismatch")
    require(isinstance(metrics.get("repair_timing"), dict), "repair timing breakdown required")
    require(metrics["repair_timing"] == repair_timing(rows, metrics["repair_timing"]), "repair timing mismatch")
    expected_workflow = execution_workflow_aggregate(rows, metrics["phases"])
    require(metrics["workflow"] == expected_workflow, "workflow metrics differ from selected turns")
    require(metrics.get("token_phase_breakdown") == token_breakdown(rows), "token phase breakdown mismatch")
    require(not {r["turn_id"] for r in rows}.intersection(e["turn_id"] for e in metrics.get("excluded_turns", [])),
            "a selected turn cannot also be excluded")
    require(set(metrics["phases"]) == set(CORE), "exactly three metric phases required")
    for phase in CORE:
        item = metrics["phases"][phase]
        if item["status"] in ("closed", "skipped"):
            expected = execution_phase_aggregate(rows, phase, metrics["repair_timing"])
            require(item["values"] == expected, f"{phase} metrics mismatch")
            if item["status"] == "skipped":
                require(phase == "repair" and bool(item.get("reason")) and not any(r["phase"] == phase for r in rows),
                        "skipped repair must have a decision and no work turns")
        else:
            require(item["values"] is None, "unclosed phase cannot report final values")
    intervals = sorted((s["start"]["epoch_ms"], s["end"]["epoch_ms"])
                       for row in rows for s in row["timing_segments"] if "end" in s)
    require(all(a[1] <= b[0] for a, b in zip(intervals, intervals[1:])), "overlapping captured time")


def metrics_markdown(metrics):
    validate_metrics(metrics)
    lines = ["## Observed workflow metrics", "", f"Status: {metrics['status']}", "",
             "| Scope | Input | Cached input | Output | Reasoning output | Total | Duration seconds | Wall-clock seconds | Turns | Tool calls |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    values = [(p, metrics["phases"][p]["values"]) for p in CORE] + [("workflow", metrics["workflow"])]
    for name, item in values:
        cells = ([item["tokens"][k] for k in USAGE] + [item["duration_seconds"], item["wall_clock_seconds"],
                 item["workflow_turn_count"], item["tool_call_count"]]) if item else [None] * 9
        lines.append("| " + name + " | " + " | ".join("N/A" if c is None else str(c) for c in cells) + " |")
    lines += ["", "Cached input is included in input; reasoning output is included in output.",
              "Duration seconds sum captured work intervals. Wall-clock seconds sum rollout durations of the same turns as tokens. "
              "Waiting between turns and measurement/report/export turns are excluded; Allow/Deny waits within selected turns are included.",
              "Model call count: unavailable (token usage updates are not model call evidence).", ""]
    lines += ["Tokens and turn/tool counts cover each whole turn by semantic phase label. "
              "Wall-clock seconds use that same label; duration seconds cover captured intervals under timing_phase.", "",
              "### Token attribution by label", "",
              "| Label | Input | Cached input | Output | Reasoning output | Total | Wall-clock seconds | Turns | Tool calls |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for phase, values in metrics["token_phase_breakdown"].items():
        cells = [values["tokens"][k] for k in USAGE] + [values["wall_clock_seconds"], values["workflow_turn_count"], values["tool_call_count"]]
        lines.append("| " + phase + " | " + " | ".join("N/A" if v is None else str(v) for v in cells) + " |")
    lines += ["", "| Turn | Token label | Timing bucket | Duration seconds | Wall-clock seconds | Reason |", "|---|---|---|---:|---:|---|"]
    for row in metrics["turns"]:
        reason = row["reason"].replace("|", "\\|").replace("\n", " ")
        core = row["duration_seconds"] if row["duration_seconds"] is not None else "N/A"
        lines.append(f"| {row['turn_id']} | {row['phase']} | {row['timing_phase']} | {core} | {row['wall_clock_seconds']} | {reason} |")
    lines.append("")
    lines += [f"Timing protocol: `{metrics['timing_protocol']}`.", "",
              ("Repair seconds include integrated BR/flow/runtime verification and final evidence persistence. "
               "A turn with core execution must retain that core token label."), "",
              "Workflow duration seconds = Prompt execution + first-pass Source execution + all Repair executions. "
              "Configuration, approvals, dataset resolution, separate audit/runtime and reporting are excluded from duration seconds. "
              "Eligible auxiliary turns contribute tokens and wall-clock time to workflow. "
              "Pending/missing duration seconds are N/A, not zero. Workflow wall-clock covers selected completed turns to date; "
              "it is final only when workflow status is finalized.", ""]
    for repair_id, item in metrics["repair_timing"].items():
        lines.append(f"- {repair_id}: {item['duration_seconds'] if item['duration_seconds'] is not None else 'N/A'} seconds")
    if metrics["phases"]["repair"]["status"] == "skipped":
        lines += ["Repair skipped: " + metrics["phases"]["repair"]["reason"], ""]
    for row in metrics["turns"]:
        if row["duration_seconds"] is None:
            lines.append(f"- Timing unavailable for `{row['turn_id']}`: {row['timing_unavailable_reason']}")
    return "\n".join(lines)
