#!/usr/bin/env python3
"""Read-only configuration selection and integrity preflight; never asks for approval."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "measure-uc-workflow/scripts"))
from metrics_contract import ROOT, digest, epoch, require, validate_canonical_path, writable, validate_metrics
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from validate_experiment_configuration import read_configuration_json as read_json, validate
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "audit-flow-accuracy/scripts"))
from score_flow_accuracy import validate_baseline as validate_flow_baseline
from database_baseline import validate_input as validate_database_input, verify_database


def check_reference(reference, path, config, checksum):
    require(isinstance(reference, dict), "configuration reference must be an object")
    require(reference.get("artifact") == path.relative_to(ROOT).as_posix(), "configuration artifact conflict")
    require(reference.get("configuration_id") == config["configuration_id"], "configuration ID conflict")
    require(reference.get("checksum") == checksum, "configuration checksum mismatch; do not edit pinned configuration")
    for field in ("comparison_group_id", "researcher_id"):
        if field in reference:
            require(reference[field] == config[field], f"configuration {field} conflict")


def check_pinned_evidence(path, config, checksum):
    relative = path.relative_to(ROOT).as_posix()
    for evidence_path in (ROOT / "docs/04-experiments").glob("*/canonical-run-*.json"):
        if evidence_path.parent.name == "configurations":
            continue
        evidence = read_json(evidence_path)
        reference = evidence.get("experiment_configuration")
        if isinstance(reference, dict) and (reference.get("artifact") == relative
                                          or reference.get("configuration_id") == config["configuration_id"]):
            check_reference(reference, path, config, checksum)
    for evidence_path in (ROOT / "docs/02-construction/implementation").glob("*/runs/*/run-activation.json"):
        evidence = read_json(evidence_path)
        if (evidence.get("configuration_artifact") == relative
                or evidence.get("configuration_id") == config["configuration_id"]):
            require(evidence.get("configuration_artifact") == relative
                    and evidence.get("configuration_checksum") == checksum, "activation configuration checksum/identity conflict")


def source_br_ids(raw):
    content = raw.decode("utf-8-sig")
    headings = list(re.finditer(r"(?m)^## Business Rules[ \t]*\r?$", content))
    require(len(headings) == 1, "frozen UC Business Rules section missing or ambiguous")
    section = content[headings[0].end():]
    following_heading = re.search(r"(?m)^## [^\r\n]+", section)
    if following_heading:
        section = section[:following_heading.start()]
    ids = re.findall(r"(?m)^BR-[A-Z]+-\d+(?=[ \t]*(?::|-)[ \t]+\S)", section)
    require(ids and len(ids) == len(set(ids)), "frozen UC BR IDs missing or duplicated")
    return ids


def source_api_ids(raw):
    content = raw.decode("utf-8-sig")
    headings = list(re.finditer(r"(?m)^### Related API IDs[ \t]*\r?$", content))
    require(headings, "frozen UC Related API IDs section missing")
    ids = []
    for heading in headings:
        section = content[heading.end():]
        following_heading = re.search(r"(?m)^###? [^\r\n]+", section)
        if following_heading:
            section = section[:following_heading.start()]
        for api_id in re.findall(r"\bAPI-[A-Z0-9]+(?:-[A-Z0-9]+)*\b", section):
            if api_id not in ids:
                ids.append(api_id)
    require(ids, "frozen UC Related API IDs are missing")
    return ids


def check_baselines(uc):
    result, baselines, source_raw = {}, [], None
    for field, kind in (("business_rule_baseline", "business-rule-baseline"), ("flow_baseline", "flow-baseline")):
        value = uc.get(field)
        require(isinstance(value, str) and value.strip(), f"missing {field}")
        path = writable(ROOT / value)
        require(path.is_relative_to(ROOT / "docs/02-construction/implementation" / uc["uc_id"]),
                f"{field} must belong to the selected UC")
        require(path.is_file(), f"missing {field}: {value}; prepare this input outside generation")
        data = read_json(path)
        require(data.get("status") == "Frozen" and data.get("artifact_type") == kind
                and data.get("uc_id") == uc["uc_id"], f"invalid {field} identity/status")
        if field == "business_rule_baseline":
            expected_fields = {"schema_version", "artifact_type", "status", "uc_id", "use_case_path",
                               "use_case_sha256", "spreadsheet_source", "ordered_br_ids", "frozen_at"}
            require(set(data) == expected_fields, "invalid BR baseline fields")
            require(data.get("schema_version") == 1, "invalid BR baseline schema")
            require(isinstance(data.get("spreadsheet_source"), str) and data["spreadsheet_source"].strip(),
                    "BR baseline spreadsheet source missing")
            epoch(data.get("frozen_at"))
            source = writable(ROOT / data.get("use_case_path", ""))
            require(source.is_file(), "BR baseline UC source missing")
            raw = source.read_bytes()
            source_raw = raw
            lf = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            expected = data.get("use_case_sha256")
            require(expected in {digest(raw), digest(lf), digest(lf.replace(b"\n", b"\r\n"))}, "BR baseline UC checksum mismatch")
            if expected != digest(raw):
                receipt = ROOT / "docs/02-construction/implementation" / uc["uc_id"] / "source-checksum-normalization.json"
                require(receipt.is_file(), "UC newline-only match requires source-checksum-normalization.json")
            source_ids = source_br_ids(raw)
            require(data["ordered_br_ids"] == source_ids, "frozen UC/BR baseline order conflict")
        else:
            validate_flow_baseline(data)
        baselines.append(data)
        result[field] = "valid"
    if len(baselines) == 2:
        require(baselines[0]["use_case_path"] == baselines[1]["use_case_path"], "BR/flow baseline UC source conflict")
    contracts = uc.get("api_contracts")
    require(isinstance(contracts, list) and contracts, "configured API contracts missing")
    configured_ids = [entry.get("api_id") for entry in contracts]
    require(configured_ids == source_api_ids(source_raw), "configuration/frozen UC API contract order mismatch")
    result["api_contracts"] = contracts
    return result


def select_canonical(uc_id, run_id=None, variant=None, configuration=None, run_json=None):
    if run_json is not None:
        path = writable(run_json)
        require(path.is_file(), f"missing Canonical Run JSON: {path}")
        candidate = read_json(path)
        validate_canonical_path(path, candidate)
        return path, candidate
    matches = []
    for path in (ROOT / "docs/04-experiments" / uc_id).glob("canonical-run-*.json"):
        candidate = read_json(path)
        if candidate.get("uc_id") != uc_id or "experiment_configuration" not in candidate:
            continue
        validate_canonical_path(path, candidate)
        if run_id is not None and candidate.get("run_id") != run_id:
            continue
        if variant is not None and candidate.get("prompt_variant") != variant:
            continue
        reference = candidate.get("experiment_configuration") or {}
        if configuration is not None and writable(ROOT / reference.get("artifact", "")) != writable(configuration):
            continue
        matches.append((path, candidate))
    require(len(matches) == 1, "Canonical Run JSON is missing or ambiguous; provide an existing --run-json; preflight never initializes it")
    return matches[0]


def check_canonical(run, config, assignment, uc, stage):
    for field in ("run_status", "metrics", "coding_prompt", "repair_authorization"):
        require(field in run, f"canonical {field} missing")
    require(run.get("metrics_schema_version") == 3, "canonical metrics_schema_version must be 3")
    require(isinstance(run.get("uc_name"), str) and run["uc_name"].strip(), "canonical uc_name missing")
    for field in ("replicate_index", "run_order"):
        require(type(run.get(field)) is int and run[field] == assignment[field], f"canonical {field} mismatch")
    require(run.get("audit_protocol") == config["audit_design"]["protocol"], "canonical audit protocol mismatch")
    model = run.get("generation_model")
    require(isinstance(model, dict), "canonical generation_model missing")
    for field in ("requested_model_id", "requested_reasoning_effort"):
        require(model.get(field) == assignment[field], f"canonical {field} mismatch")
    for field in ("requested_label", "requested_reasoning_mode"):
        if field in model:
            require(model[field] == assignment[field], f"canonical {field} mismatch")
    business = run.get("business_rules")
    baseline = read_json(writable(ROOT / uc["business_rule_baseline"]))
    require(isinstance(business, dict) and business.get("baseline") == uc["business_rule_baseline"]
            and business.get("ordered_br_ids") == baseline.get("ordered_br_ids"), "canonical BR baseline/IDs mismatch")
    expected_activation = f"docs/02-construction/implementation/{run['uc_id']}/runs/{run['run_id']}/run-activation.json"
    require(run["experiment_configuration"].get("run_activation") in (None, expected_activation),
            "canonical activation path mismatch")
    require(isinstance(run.get("repairs"), list), "canonical repairs must be an array")
    approval = run.get("repair_authorization")
    require(isinstance(approval, dict) and type(approval.get("approved")) is bool,
            "canonical repair_authorization invalid")
    metrics = run.get("metrics")
    if metrics is not None:
        validate_metrics(metrics)
        require(all(metrics.get(k) == run[k] for k in ("uc_id", "run_id")), "canonical telemetry identity mismatch")
    gates = run.get("gates")
    require(isinstance(gates, dict), "canonical gate state missing")
    # Imported lazily because gate validation also imports the prompt validator.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "advance-experiment-gate/scripts"))
    from record_gate import validate_gate_history
    validate_gate_history(gates, "prompt" if stage == "prompt" else "source")
    if stage == "prompt":
        require(run.get("run_status") == "draft", "prompt requires canonical run_status: draft")
        require(run.get("coding_prompt") is None, "prompt is already approved or canonical coding_prompt is not null")
        require(not run["repairs"], "prompt run already contains repairs")
        require(approval["approved"] is False, "prompt run cannot already authorize repair")
        require(business.get("initial") is None and business.get("final") is None,
                "prompt run cannot contain source audit results")
        require(metrics is None or metrics.get("phases", {}).get("prompt_generation", {}).get("status") != "closed",
                "prompt phase is already closed")
    else:
        require(isinstance(metrics, dict) and metrics.get("phases", {}).get("prompt_generation", {}).get("status") == "closed",
                "source/activation requires closed prompt telemetry")
        require(run.get("run_status") not in {"complete", "stopped", "repair_declined"}, "run is terminal")


def preflight(uc_id, configuration=None, run_id=None, variant=None, run_json=None,
              expected_checksum=None, stage="prompt", use_case=None):
    require(stage in {"prompt", "activation", "source"}, "invalid preflight stage")
    require(isinstance(uc_id, str) and uc_id and all(c.isalnum() or c in "-_." for c in uc_id)
            and uc_id not in {".", ".."}, "invalid UC ID")
    canonical_path, canonical = select_canonical(uc_id, run_id, variant, configuration, run_json)
    canonical_checksum = digest(canonical_path.read_bytes())
    if canonical is not None:
        require(canonical.get("uc_id") == uc_id, "canonical UC mismatch")
        require(run_id is None or run_id == canonical.get("run_id"), "canonical run mismatch")
        run_id = canonical.get("run_id")
        require(isinstance(run_id, str) and run_id, "canonical run ID missing")
        reference = canonical.get("experiment_configuration") or {}
        pinned_path = writable(ROOT / reference.get("artifact", ""))
        require(configuration is None or writable(configuration) == pinned_path, "canonical configuration mismatch")
        configuration = pinned_path
    paths = [writable(configuration)] if configuration else sorted((ROOT / "docs/04-experiments/configurations").glob("*.json"))
    matches = []
    for path in paths:
        original_checksum = digest(path.read_bytes())
        data = read_json(path)
        if configuration is None and (not isinstance(data.get("use_case"), dict)
                                      or data["use_case"].get("uc_id") != uc_id):
            continue
        data = validate(path)
        require(digest(path.read_bytes()) == original_checksum, "configuration changed during validation")
        for assignment in data["runs"]:
            if assignment["uc_id"] == uc_id and (run_id is None or assignment["run_id"] == run_id):
                if variant is None or assignment.get("prompt_variant") == variant:
                    matches.append((path, data, assignment, original_checksum))
    require(len(matches) == 1, "configuration/UC/run selection is missing, conflicting or ambiguous; provide exact --configuration and --run-id")
    path, data, assignment, checksum = matches[0]
    require(expected_checksum is None or checksum == expected_checksum, "configuration changed since preflight")
    if canonical is not None:
        check_reference(canonical.get("experiment_configuration"), path, data, checksum)
        require(canonical.get("prompt_variant") == assignment.get("prompt_variant"), "canonical variant mismatch")
    check_pinned_evidence(path, data, checksum)
    uc = data["use_case"]
    baselines = check_baselines(uc)
    check_canonical(canonical, data, assignment, uc, stage)
    # Fifth prepared input: ordered migration history/head and DBML/runtime hashes.
    # Never initialize migrations or derive replacement pins from the live DB.
    # Activation/Measure uses this preflight too: it must remain offline.
    if stage in {"prompt", "source"}:
        verify_database(data)
    else:
        validate_database_input(data)
    baseline = read_json(writable(ROOT / uc["business_rule_baseline"]))
    if use_case is not None:
        require(writable(use_case) == writable(ROOT / baseline["use_case_path"]), "requested UC path differs from frozen baseline")
    if stage in {"activation", "source"}:
        from validate_prompt_contract import validate_prompt
        prompt_ref = canonical.get("coding_prompt") or {}
        prompt_path = writable(ROOT / prompt_ref.get("path", ""))
        require(prompt_path.is_file() and digest(prompt_path.read_bytes()) == prompt_ref.get("sha256"),
                "canonical approved prompt path/checksum mismatch")
        activation_path = ROOT / "docs/02-construction/implementation" / uc_id / "runs" / assignment["run_id"] / "run-activation.json"
        activation = activation_path if stage == "source" and activation_path.is_file() else None
        validate_prompt(path, uc_id, assignment["run_id"], prompt_path, activation=activation)
    require(digest(path.read_bytes()) == checksum, "configuration changed during preflight")
    require(digest(canonical_path.read_bytes()) == canonical_checksum, "Canonical Run JSON changed during preflight")
    return {"status": "valid", "uc_id": uc_id, "run_id": assignment["run_id"],
            "prompt_variant": assignment.get("prompt_variant"),
            "experiment_configuration": {"artifact": path.relative_to(ROOT).as_posix(),
                                         "configuration_id": data["configuration_id"], "checksum": checksum,
                                         "comparison_group_id": data["comparison_group_id"],
                                         "researcher_id": data["researcher_id"],
                                         "run_activation": f"docs/02-construction/implementation/{uc_id}/runs/{assignment['run_id']}/run-activation.json"},
            "canonical_run": {"path": canonical_path.relative_to(ROOT).as_posix(), "sha256": canonical_checksum},
            "stage": stage, "baselines": baselines}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uc-id", required=True)
    parser.add_argument("--configuration", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--variant")
    parser.add_argument("--run-json", type=Path)
    parser.add_argument("--use-case", type=Path)
    parser.add_argument("--stage", choices=("prompt", "activation", "source"), default="prompt")
    parser.add_argument("--expected-checksum")
    args = parser.parse_args()
    print(json.dumps(preflight(**vars(args)), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        raise SystemExit(f"configuration preflight blocked: {exc}")
