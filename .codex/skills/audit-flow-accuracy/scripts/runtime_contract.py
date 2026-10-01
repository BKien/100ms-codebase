"""Structural validation for completion-critical-flow-runtime-v2 (no execution)."""

import sys
from pathlib import Path

from metrics_contract import ROOT, epoch, read_json, require, writable

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from validate_experiment_configuration import validate as validate_configuration

RUNTIME_RUBRIC = "completion-critical-flow-runtime-v2"
RUNTIME_KINDS = {"ui", "network", "backend", "data", "runtime_trace"}
STATIC_KINDS = {"source", "build", "health", "deployment", "limitation"}
IDENTITY = ("uc_id", "run_id", "stage", "source_revision")


def method(data):
    version = data.get("schema_version")
    require(type(version) is int and version == 2, "unsupported flow schema")
    rubric = data.get("rubric_id")
    require(rubric == RUNTIME_RUBRIC, "flow schema/rubric mismatch")
    return version, rubric


def configured_rubric(run, folder, validate_evidence, baseline=None):
    """Resolve the pinned configuration; validate optional activation."""
    metadata = run.get("experiment_configuration") or {}
    activation_path = folder / "run-activation.json"
    require(metadata, "pinned experiment configuration required")
    activation = read_json(activation_path) if activation_path.exists() else None
    if activation is not None:
        require(activation.get("status") == "Confirmed", "run activation must be Confirmed")
        require(all(activation.get(k) == run.get(k) for k in ("uc_id", "run_id")), "activation identity mismatch")
        ref = {"path": activation.get("configuration_artifact"), "sha256": activation.get("configuration_checksum")}
    else:
        ref = {"path": metadata.get("artifact"), "sha256": metadata.get("checksum")}
    config_path = validate_evidence(ref)
    config = validate_configuration(config_path)
    require(config.get("status") == "Confirmed", "flow rubric requires Confirmed configuration")
    if metadata:
        require(metadata.get("artifact") == ref["path"] and metadata.get("checksum") == ref["sha256"],
                "run/configuration reference mismatch")
    require(sum(r.get("uc_id") == run["uc_id"] and r.get("run_id") == run["run_id"]
                for r in config.get("runs", [])) == 1, "configured run assignment mismatch")
    version = config.get("schema_version")
    require(version == "2.4", "unknown configuration schema")
    rubric = config.get("flow_audit_rubric")
    require(rubric == RUNTIME_RUBRIC,
            "configuration flow rubric mismatch")
    if baseline is not None:
        configured_uc = config.get("use_case")
        require(isinstance(configured_uc, dict) and configured_uc.get("uc_id") == run["uc_id"]
                and baseline["path"] == configured_uc.get("flow_baseline"),
                "assessment must use the configured flow baseline")
        baseline_data = read_json(validate_evidence(baseline))
        if activation is not None:
            require(epoch(baseline_data.get("frozen_at")) <= epoch(activation.get("activated_at")),
                    "flow baseline must be frozen before run activation")
    return rubric


def validate_runtime(data, definitions, validate_evidence):
    """Return validated attempts and a validator for target-specific references."""
    root = writable(ROOT / "docs/02-construction/implementation" / data["uc_id"] /
                    "runs" / data["run_id"] / "flow-accuracy/evidence" / data["assessment_id"])
    for key in ("uc_id", "run_id"):
        require(isinstance(data[key], str) and data[key] not in (".", "..") and
                all(c.isalnum() or c in "-_." for c in data[key]), f"unsafe {key}")

    def artifact(ref):
        path = validate_evidence(ref)
        require(not Path(ref["path"]).is_absolute(), "v2 evidence paths must be repository-relative")
        require(path.is_relative_to(root), "v2 evidence must be preserved under this assessment's evidence directory")
        require(ref.get("kind") in RUNTIME_KINDS | STATIC_KINDS, "unknown evidence kind")
        require(ref.get("source_revision") == data["source_revision"], "evidence source revision mismatch")
        require(ref.get("sanitized") is True, "evidence must be sanitized before hashing")
        require(isinstance(ref.get("locator"), str) and ref["locator"].strip(), "evidence locator required")
        if ref["kind"] == "source":
            provenance = ref.get("provenance") or {}
            require(isinstance(provenance.get("path"), str) and provenance["path"].strip(), "source original path required")
            writable(ROOT / provenance["path"])
            require(isinstance(provenance.get("locator"), str) and provenance["locator"].strip(), "source original locator required")
        return path

    runtime = data.get("runtime")
    require(isinstance(runtime, dict), "runtime record required")
    for limitation in data["limitations"]:
        require(isinstance(limitation, dict) and limitation.get("category") in
                {"application", "environment", "missing_evidence", "ambiguous_cause"}, "invalid limitation category")
        require(all(isinstance(limitation.get(k), str) and limitation[k].strip() for k in ("affected_targets", "reason", "impact")),
                "limitation needs affected targets, reason and impact")
    require(runtime.get("status") in {"ready", "BLOCKED", "unverified"}, "invalid runtime status")
    require(
        runtime.get("compose_version") in {2, 5},
        "Docker Compose v2-compatible CLI required (major 2 or 5); no host fallback",
    )
    require(isinstance(runtime.get("reason"), str) and runtime["reason"].strip(), "runtime reason required")
    deployment = runtime.get("deployment")
    require(isinstance(deployment, dict), "deployment linkage required")
    require(deployment.get("source_revision") == data["source_revision"], "deployment revision mismatch")
    require(type(deployment.get("verified")) is bool, "deployment verification flag required")
    deployment_refs = deployment.get("evidence")
    require(isinstance(deployment_refs, list) and deployment_refs, "deployment or blocker evidence required")
    for ref in deployment_refs:
        artifact(ref)
        require(ref["kind"] in {"deployment", "limitation"} and ref.get("observation_id") is None,
                "deployment evidence must be assessment-scoped")
    if runtime["status"] == "ready":
        require(deployment["verified"] and any(r["kind"] == "deployment" for r in deployment_refs),
                "ready runtime requires deployment evidence")
        require(isinstance(runtime.get("compose_project"), str) and runtime["compose_project"].strip(), "Compose project required")
        services = runtime.get("services")
        require(isinstance(services, list) and services, "deployed services required")
        for service in services:
            require(isinstance(service, dict) and all(isinstance(service.get(k), str) and service[k].strip()
                    for k in ("name", "container_id", "image_id", "state")), "service identity/state required")

    attempts = data.get("observations")
    require(isinstance(attempts, list), "observations array required even when blocked")
    by_id = {}
    definition_map = {f["flow_id"]: f for f in definitions}
    all_steps = {s["step_id"] for f in definitions for s in f["steps"]}

    def refs_for(refs, attempt, target=None):
        require(isinstance(refs, list) and refs, "observation evidence required")
        for ref in refs:
            artifact(ref)
            require(ref.get("observation_id") == attempt["observation_id"], "evidence observation mismatch")
            require(ref.get("flow_id") == attempt["flow_id"], "evidence flow mismatch")
            require(ref["kind"] in RUNTIME_KINDS, "runtime observation needs behavioral evidence")
            require((root / attempt["observation_id"]).resolve() in validate_evidence(ref).parents,
                    "attempt evidence must stay in its observation directory")
            captured = epoch(ref.get("captured_at"))
            require(epoch(attempt["started_at"]) <= captured <= epoch(attempt["ended_at"]), "evidence outside observation interval")
            targets = ref.get("target_ids")
            require(isinstance(targets, list) and targets and all(t in all_steps | {"entry", "branch", "terminal_outcome"} for t in targets),
                    "invalid evidence target IDs")
            if target is not None:
                require(target in targets, "evidence does not cover target")
            if ref.get("absence") is not None:
                absence = ref["absence"]
                require(ref["kind"] == "network" and isinstance(absence, dict), "absence requires network capture scope")
                require(all(isinstance(absence.get(k), str) and absence[k].strip() for k in ("scope", "capture_method")),
                        "absence scope/capture method required; missing logs are insufficient")
                require(epoch(attempt["started_at"]) <= epoch(absence.get("started_at")) <= epoch(absence.get("ended_at")) <= epoch(attempt["ended_at"]),
                        "invalid absence observation interval")

    for attempt in attempts:
        require(isinstance(attempt, dict), "observation must be an object")
        oid = attempt.get("observation_id")
        require(isinstance(oid, str) and oid not in ("", ".", "..") and all(c.isalnum() or c in "-_." for c in oid), "unsafe observation ID")
        require(oid not in by_id, "duplicate observation ID")
        by_id[oid] = attempt
        require(all(attempt.get(k) == data[k] for k in IDENTITY), "observation UC/run/stage/revision mismatch")
        require(attempt.get("baseline") == data["baseline"], "observation baseline mismatch")
        require(attempt.get("flow_id") in definition_map, "unknown observation flow")
        require(attempt.get("state") in {"completed", "incomplete", "blocked"}, "invalid observation end state")
        for key in ("actual_preconditions", "entry_point", "end_state", "scope"):
            require(isinstance(attempt.get(key), str) and attempt[key].strip(), f"observation {key} required")
        require(attempt.get("entry_kind") in {"ui", "api", "other"}, "invalid entry kind")
        start, end = epoch(attempt.get("started_at")), epoch(attempt.get("ended_at"))
        limit = attempt.get("time_limit_seconds")
        require(type(limit) is int and limit > 0, "positive observation time limit required")
        require(epoch(attempt.get("planned_at")) <= start <= end <= epoch(data["captured_at"]), "invalid observation chronology")
        require(end - start <= limit * 1000, "observation exceeded declared bound")
        actions = attempt.get("actions")
        require(isinstance(actions, list) and actions, "linked action sequence required")
        previous = start
        for index, action in enumerate(actions):
            require(isinstance(action, dict) and action.get("sequence") == index + 1, "action order mismatch")
            at = epoch(action.get("at"))
            require(previous <= at <= end, "action outside chronological sequence")
            previous = at
            require(all(isinstance(action.get(k), str) and action[k].strip() for k in ("action", "actual_result")), "actual action/result required")
            targets = action.get("target_ids")
            require(isinstance(targets, list) and targets, "action baseline targets required")
            for target in targets:
                refs_for(action.get("evidence"), attempt, target)
            for ref in action["evidence"]:
                if ref.get("absence") is not None:
                    require(epoch(ref["absence"]["started_at"]) <= at <= epoch(ref["absence"]["ended_at"]),
                            "absence capture must span the relevant action")
        require("entry" in actions[0]["target_ids"], "observation must start at specified entry")
        if attempt["entry_kind"] == "ui":
            require(any(r["kind"] == "ui" for r in actions[0]["evidence"]), "UI entry cannot be replaced by direct API")
        if attempt["state"] == "completed":
            require(runtime["status"] == "ready" and deployment["verified"], "completed observation needs verified deployment")
            require("terminal_outcome" in actions[-1]["target_ids"], "completed chain needs terminal outcome")
            if definition_map[attempt["flow_id"]]["type"] != "main":
                require(any("branch" in a["target_ids"] for a in actions), "branch condition must be observed")

    def validate_target(item, target, flow_id, critical):
        for ref in item["evidence"]:
            artifact(ref)
            if ref["kind"] in RUNTIME_KINDS:
                attempt = by_id.get(ref.get("observation_id"))
                require(attempt is not None and attempt["flow_id"] == flow_id, "missing/wrong observation reference")
                refs_for([ref], attempt, target)
                if item["status"] != "not_evaluable":
                    require(runtime["status"] == "ready" and deployment["verified"], "runtime verdict requires verified source/deployment")
                require(any(target in a["target_ids"] and ref in a["evidence"] for a in attempt["actions"]),
                        "target evidence missing from action sequence")
            else:
                require(ref.get("observation_id") is None, "static evidence cannot claim runtime observation")
        findings = item.get("source_findings")
        require(isinstance(findings, list), "separate source_findings array required")
        for finding in findings:
            require(isinstance(finding, dict) and all(isinstance(finding.get(k), str) and finding[k].strip()
                    for k in ("finding", "limits")), "source finding and limits required")
            require(isinstance(finding.get("evidence"), list) and finding["evidence"], "source finding evidence required")
            for ref in finding["evidence"]:
                artifact(ref)
                require(ref["kind"] == "source" and ref.get("observation_id") is None, "source finding needs static snapshot")
        if critical and item["status"] == "met":
            kinds = item.get("required_runtime_kinds")
            require(isinstance(kinds, list) and kinds and set(kinds) <= RUNTIME_KINDS, "critical met needs frozen-requirement-derived runtime evidence kinds")
            require(isinstance(item.get("evidence_requirement_rationale"), str) and item["evidence_requirement_rationale"].strip(),
                    "explain required evidence from frozen behavior")
            oid = item.get("observation_id")
            require(oid in by_id and by_id[oid]["flow_id"] == flow_id, "critical met needs a matching observation")
            require(runtime["status"] == "ready" and deployment["verified"], "critical met needs verified runtime")
            require(set(kinds) <= {r["kind"] for r in item["evidence"] if r.get("observation_id") == oid},
                    "critical met lacks required runtime evidence")
    return by_id, validate_target


def complete_chain(assessed, definition, attempts):
    oid = assessed.get("completion_observation_id")
    if oid is None:
        return False
    attempt = attempts.get(oid)
    require(attempt is not None and attempt["flow_id"] == definition["flow_id"], "unknown/wrong completion observation")
    targets = [s for s, d in zip(assessed["steps"], definition["steps"]) if d["completion_critical"]]
    targets.append(assessed["terminal_outcome"])
    return attempt["state"] == "completed" and all(t.get("observation_id") == oid for t in targets)
