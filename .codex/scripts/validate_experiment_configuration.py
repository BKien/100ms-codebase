#!/usr/bin/env python3
"""Validate a confirmed Business Rule experiment configuration."""

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

EFFORTS = {"none", "low", "medium", "high", "xhigh", "max"}
MODES = {"standard", "pro"}
PROTOCOLS = {"fixed", "matched", "cross"}
SCHEMA_VERSION = "2.4"
TIMING_METHOD = "system_timestamp_delta"
RUNTIME_FLOW_RUBRIC = "completion-critical-flow-runtime-v2"
ROOT = Path(__file__).resolve().parents[2]


def unique_object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f"duplicate JSON field: {key}")
        data[key] = value
    return data


def invalid_constant(value):
    raise ValueError(f"non-finite JSON value: {value}")


def read_configuration_json(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object,
                      parse_constant=invalid_constant)
    if not isinstance(data, dict):
        raise ValueError(f"JSON object required: {path}")
    return data


def flow_rubric(data):
    expected = RUNTIME_FLOW_RUBRIC
    actual = data.get("flow_audit_rubric")
    if actual != expected:
        raise ValueError("flow_audit_rubric does not match configuration schema")
    return actual


def text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    if "<" in value or ">" in value:
        raise ValueError(f"{field} contains an unresolved template placeholder")
    return value.strip()


def positive(value, field):
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{field} must be a positive integer")
    return value


def identifier(value, field):
    value = text(value, field)
    if value in {".", ".."} or not all(c.isalnum() or c in "-_." for c in value):
        raise ValueError(f"{field} must be a safe identifier, not a path")
    return value


def validate_model(model, field):
    if not isinstance(model, dict):
        raise ValueError(f"{field} must be an object")
    text(model.get("requested_label"), field + ".requested_label")
    text(model.get("requested_model_id"), field + ".requested_model_id")
    if text(model.get("requested_reasoning_effort"), field + ".requested_reasoning_effort") not in EFFORTS:
        raise ValueError(f"{field} has invalid reasoning effort")
    if text(model.get("requested_reasoning_mode"), field + ".requested_reasoning_mode") not in MODES:
        raise ValueError(f"{field} has invalid reasoning mode")


def frozen_api_contract(entry, field):
    if not isinstance(entry, dict) or set(entry) != {"api_id", "path", "sha256"}:
        raise ValueError(f"{field} must contain exactly api_id, path and sha256")
    api_id = identifier(entry.get("api_id"), field + ".api_id")
    path_value = text(entry.get("path"), field + ".path").replace("\\", "/")
    if entry.get("path") != path_value or Path(path_value).is_absolute():
        raise ValueError(f"{field}.path must be a canonical repository-relative path")
    path = (ROOT / path_value).resolve()
    api_root = (ROOT / "docs/01-inception/api-contracts").resolve()
    if not path.is_relative_to(api_root) or path.suffix.lower() != ".md":
        raise ValueError(f"{field}.path must identify a Markdown API contract under docs/01-inception/api-contracts")
    if not path.is_file():
        raise ValueError(f"{field}.path does not exist")
    expected = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    if entry.get("sha256") != expected:
        raise ValueError(f"{field}.sha256 mismatch")
    content = path.read_text(encoding="utf-8-sig")
    frontmatter = re.match(r"\A---\s*\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.S)
    if frontmatter is None:
        raise ValueError(f"{field} API contract frontmatter missing")
    metadata = {}
    for line in frontmatter.group(1).splitlines():
        match = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
        if match:
            metadata[match.group(1)] = match.group(2)
    if (metadata.get("artifact_type") != "api-contract" or metadata.get("status") != "Frozen"
            or metadata.get("api_id") != api_id):
        raise ValueError(f"{field} API contract identity/status mismatch")
    return {"api_id": api_id, "path": path_value, "sha256": expected}


def validate(path):
    path = path.resolve()
    if not path.is_relative_to(ROOT / "docs/04-experiments/configurations"):
        raise ValueError("configuration must be stored under docs/04-experiments/configurations")
    data = read_configuration_json(path)
    schema_version = data.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    rubric = flow_rubric(data)
    if data.get("artifact_type") != "experiment-configuration" or data.get("status") != "Confirmed":
        raise ValueError("configuration must be Confirmed")
    for field in ("configuration_id", "comparison_group_id", "researcher_id", "decided_at", "sheet_revision"):
        text(data.get(field), field)
    configuration_id = identifier(data["configuration_id"], "configuration_id")
    if path.name != f"{configuration_id}.json":
        raise ValueError("configuration filename must equal <configuration_id>.json")
    decided = datetime.fromisoformat(data["decided_at"].replace("Z", "+00:00"))
    if decided.tzinfo is None:
        raise ValueError("decided_at must include a timezone")
    timing_method = data.get("timing_method")
    if timing_method != TIMING_METHOD:
        raise ValueError(f"schema {schema_version} timing_method must be {TIMING_METHOD}")
    # Offline database contract: migration_head, dbml_sha256, schema_fingerprint_sha256.
    # Runtime history/drift checks belong to generation/audit, never Measure.
    sys.path.insert(0, str(ROOT / ".codex/skills/gen-coding-prompt/scripts"))
    from database_baseline import validate_input
    validate_input(data)
    figma = data.get("figma_dataset")
    if not isinstance(figma, dict):
        raise ValueError(f"schema {schema_version} requires figma_dataset")
    version = text(figma.get("dataset_version"), "figma_dataset.dataset_version")
    manifest_value = text(figma.get("manifest_path"), "figma_dataset.manifest_path")
    expected_path = f"resource/figma-design-dataset/{version}/manifest.json"
    if manifest_value.replace("\\", "/") != expected_path:
        raise ValueError("figma_dataset manifest path/version mismatch")
    manifest_path = (ROOT / manifest_value).resolve()
    if not manifest_path.is_relative_to(ROOT / "resource/figma-design-dataset"):
        raise ValueError("figma_dataset manifest must stay inside the dataset directory")
    if not manifest_path.is_file():
        raise ValueError("figma_dataset manifest does not exist")
    expected_hash = "sha256:" + hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if figma.get("manifest_sha256") != expected_hash:
        raise ValueError("figma_dataset manifest checksum mismatch")
    manifest = read_configuration_json(manifest_path)
    if manifest.get("dataset_version") != version or manifest.get("overall_status") != "complete":
        raise ValueError("figma_dataset must reference a complete matching version")
    audit = data.get("audit_design")
    if not isinstance(audit, dict) or audit.get("protocol") not in PROTOCOLS:
        raise ValueError("audit_design.protocol is invalid")
    if audit["protocol"] == "fixed":
        validate_model(audit.get("fixed_auditor"), "audit_design.fixed_auditor")

    if "use_cases" in data:
        raise ValueError("configuration must use one use_case object, not a use_cases array")
    uc = data.get("use_case")
    expected_uc_fields = {"uc_id", "business_rule_baseline", "flow_baseline", "api_contracts"}
    if not isinstance(uc, dict) or set(uc) != expected_uc_fields:
        raise ValueError("use_case must contain exactly uc_id, business_rule_baseline, flow_baseline and api_contracts")
    configured_uc_id = identifier(uc.get("uc_id"), "use_case.uc_id")
    text(uc.get("business_rule_baseline"), "use_case.business_rule_baseline")
    text(uc.get("flow_baseline"), "use_case.flow_baseline")
    contracts = uc.get("api_contracts")
    if not isinstance(contracts, list) or not contracts:
        raise ValueError("use_case.api_contracts must be a non-empty array")
    frozen = [frozen_api_contract(entry, f"use_case.api_contracts[{api_index}]")
              for api_index, entry in enumerate(contracts)]
    api_ids = [entry["api_id"] for entry in frozen]
    api_paths = [entry["path"] for entry in frozen]
    if len(api_ids) != len(set(api_ids)) or len(api_paths) != len(set(api_paths)):
        raise ValueError("use_case.api_contracts contains duplicate IDs or paths")

    runs = data.get("runs")
    if not isinstance(runs, list) or len(runs) != 1:
        raise ValueError("runs must contain exactly one run assignment")
    run_ids, orders, assignments = set(), set(), set()
    for index, run in enumerate(runs):
        prefix = f"runs[{index}]"
        if not isinstance(run, dict):
            raise ValueError(f"{prefix} must be an object")
        run_id = identifier(run.get("run_id"), prefix + ".run_id")
        if configuration_id != f"CFG-{run_id}":
            raise ValueError("configuration_id must equal CFG-<run_id>")
        run_uc_id = identifier(run.get("uc_id"), prefix + ".uc_id")
        if run_id in run_ids or run_uc_id != configured_uc_id:
            raise ValueError(f"{prefix} has duplicate run ID or does not belong to the configured UC")
        run_ids.add(run_id)
        order = positive(run.get("run_order"), prefix + ".run_order")
        if order in orders:
            raise ValueError(f"duplicate run_order: {order}")
        orders.add(order)
        replicate = positive(run.get("replicate_index"), prefix + ".replicate_index")
        validate_model(run, prefix)
        variant = identifier(run.get("prompt_variant"), prefix + ".prompt_variant")
        if run["prompt_variant"] != variant:
            raise ValueError(f"{prefix}.prompt_variant must be a canonical identifier")
        model_label = identifier(run.get("requested_label"), prefix + ".requested_label")
        if run["requested_label"] != model_label:
            raise ValueError(f"{prefix}.requested_label must be a canonical identifier")
        if run_id != f"{run_uc_id}-{model_label}-{variant}":
            raise ValueError(f"{prefix}.run_id must equal <UC-ID>-<MODEL>-<VARIANT> using requested_label as MODEL")
        key = (run_uc_id, variant, run["requested_model_id"], run["requested_reasoning_effort"], run["requested_reasoning_mode"], replicate)
        if key in assignments:
            raise ValueError(f"duplicate UC/variant/model/replicate assignment: {key}")
        assignments.add(key)
        text(run.get("auditor_assignment"), prefix + ".auditor_assignment")
        if "flow_audit_rubric" in run and run["flow_audit_rubric"] != rubric:
            raise ValueError("run-level rubric cannot override comparison-group rubric")
    # One evidence standard across matched runs, including other configurations in the group.
    for peer_path in path.parent.glob("*.json"):
        if peer_path.resolve() == path.resolve():
            continue
        peer = read_configuration_json(peer_path)
        if peer.get("artifact_type") == "experiment-configuration" and peer.get("configuration_id") == data["configuration_id"]:
            raise ValueError("duplicate configuration_id; select a unique immutable configuration")
        if (peer.get("artifact_type") == "experiment-configuration" and peer.get("status") == "Confirmed"
                and peer.get("comparison_group_id") == data["comparison_group_id"] and flow_rubric(peer) != rubric):
            raise ValueError("comparison group mixes flow audit rubrics; use a new comparison_group_id")
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_experiment_configuration.py <configuration.json>")
    try:
        result = validate(Path(sys.argv[1]))
        print(json.dumps({"status": "valid", "configuration_id": result["configuration_id"], "flow_audit_rubric": flow_rubric(result), "uc_id": result["use_case"]["uc_id"], "runs": len(result["runs"])}, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        raise SystemExit(f"experiment configuration error: {exc}")
