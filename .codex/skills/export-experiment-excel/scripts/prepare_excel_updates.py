#!/usr/bin/env python3
"""Resolve an AI-inspected Excel mapping into traceable scalar updates; no XLSX writes."""

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "measure-uc-workflow/scripts"))
from metrics_contract import (ROOT, atomic_write, digest, read_json, require,
                              validate_canonical_path, validate_metrics, writable)

IDENTITY = {"uc_id", "run_id", "prompt_variant", "replicate_index", "run_order", "generation_model.requested_model_id"}


def path_parts(field):
    """Decode data-only paths without restricting metric families or evaluating code."""
    require(isinstance(field, str) and field, "missing or ambiguous field")
    if field.startswith("/"):
        parts = field[1:].split("/")
        require(all(re.search(r"~(?![01])", part) is None for part in parts), "invalid JSON pointer escape")
        return [part.replace("~1", "/").replace("~0", "~") for part in parts]
    parts = field.split(".")
    require(all(re.fullmatch(r"[A-Za-z0-9_]+", part) for part in parts), "invalid JSON path")
    return parts


def lookup(record, field):
    for part in path_parts(field):
        if isinstance(record, dict) and part in record:
            record = record[part]
        elif isinstance(record, list) and re.fullmatch(r"0|[1-9][0-9]*", part) and int(part) < len(record):
            record = record[int(part)]
        else:
            raise ValueError(f"missing field: {field}")
    return record


def resolve_value(record, field, kind, conversion, source_unit=None):
    parts = path_parts(field)
    if parts[0] == "metrics":
        metrics = record.get("metrics")
        require(isinstance(metrics, dict) and metrics.get("schema_version") == 3, "no phase-aware finalized metrics")
        validate_metrics(metrics)
        require(metrics.get("uc_id") == record.get("uc_id") and metrics.get("run_id") == record.get("run_id"),
                "metrics/run identity mismatch")
        require(metrics.get("status") == "finalized", "workflow metrics are not finalized")
        if len(parts) >= 4 and parts[1] == "phases" and parts[3] == "values":
            phase = metrics["phases"][parts[2]]
            require(phase.get("status") == "closed" or
                    (parts[2] == "repair" and phase.get("status") == "skipped"),
                    phase.get("reason") or "phase is not closed")
    value = lookup(record, field)
    require(value is not None, f"null/unavailable source value: {field}")
    require(not isinstance(value, str) or value.strip(), f"empty source value: {field}")
    allowed = {"number": type(value) in (int, float), "integer": type(value) is int,
               "string": isinstance(value, str), "boolean": type(value) is bool}
    require(allowed.get(kind, False), f"source type does not match {kind}")
    if type(value) in (int, float):
        require(math.isfinite(value), "non-finite numeric value")
    if conversion == "seconds_to_minutes":
        require((parts[-1].endswith("_seconds") or source_unit == "seconds") and kind == "number"
                and type(value) in (int, float) and value >= 0, "seconds conversion requires nonnegative seconds")
        value /= 60
    elif conversion == "percent_to_fraction":
        require((parts[-1].endswith("_percent") or source_unit == "percent_points") and kind == "number"
                and type(value) in (int, float) and 0 <= value <= 100, "percent conversion requires 0..100 percent field")
        value /= 100
    else:
        require(conversion == "identity", "unknown conversion")
    return value


def prepare(mapping):
    require(mapping.get("schema_version") == 1, "unknown mapping schema")
    export_mode = mapping.get("export_mode")
    require(export_mode == "dynamic_semantic", "unknown export mode")
    requested_uc = mapping.get("requested_uc_id")
    target_sheet = mapping.get("target_sheet")
    require(isinstance(requested_uc, str) and re.fullmatch(r"UC-[0-9]+(?:\.[0-9]+)?", requested_uc), "canonical requested_uc_id required")
    require(isinstance(target_sheet, str) and target_sheet.strip(), "exact target_sheet required")
    require(isinstance(mapping.get("header_coverage"), list) and mapping["header_coverage"], "header coverage required")
    require(Path(mapping["repo_root"]).resolve() == ROOT, "repo_root must be the Business repository")
    workbook = (ROOT / mapping["workbook"]).resolve()
    require(workbook.is_file() and workbook.suffix.lower() == ".xlsx", "existing .xlsx workbook required")
    require(digest(workbook.read_bytes()) == mapping["workbook_sha256"], "workbook changed since inspection")
    require(isinstance(mapping.get("sources"), list), "canonical source candidate list required")
    sources, errors, seen_sources = [], [], set()
    for source in mapping["sources"]:
        path = writable(ROOT / source)
        candidate_run_id = path.stem.removeprefix("canonical-run-")
        require(path not in seen_sources, "duplicate source path")
        seen_sources.add(path)
        require(path.is_relative_to(ROOT / "docs/04-experiments") and path.parent.parent == ROOT / "docs/04-experiments"
                and path.parent.name != "configurations" and path.suffix == ".json", "source must be canonical UC/run JSON")
        require(path.parent.name == requested_uc, "source outside requested UC")
        try:
            raw = path.read_bytes()
            record = json.loads(raw.decode("utf-8-sig"))
            require(isinstance(record, dict) and record.get("uc_id") == path.parent.name,
                    "canonical path/identity mismatch")
            validate_canonical_path(path, record)
            metrics = record.get("metrics")
            require(isinstance(metrics, dict), "canonical run has no measured metrics")
            validate_metrics(metrics)
            require(metrics.get("status") == "finalized", "workflow metrics are not finalized; run finalize-workflow first")
            require(all(item.get("status") in ("closed", "skipped") for item in metrics["phases"].values()),
                    "finalized workflow contains an unclosed phase")
            require(metrics.get("uc_id") == record.get("uc_id") and metrics.get("run_id") == record.get("run_id"),
                    "metrics/run identity mismatch")
            sources.append((str(path), digest(raw), record))
        except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError, ArithmeticError) as error:
            errors.append({"path": str(path), "uc_id": path.parent.name,
                           "run_id": candidate_run_id, "reason": str(error)})
    updates, seen = [], set()
    require(isinstance(mapping.get("cells"), list) and mapping["cells"], "no writable result cells identified; report unresolved destinations without exporting")
    for cell in mapping["cells"]:
        require(isinstance(cell.get("sheet"), str) and cell["sheet"], "sheet required")
        require(cell["sheet"] == target_sheet, "cell outside requested tab")
        require(re.fullmatch(r"[A-Z]{1,3}[1-9][0-9]{0,6}", cell.get("cell", "")), "single A1 cell required")
        key = (cell["sheet"], cell["cell"])
        require(key not in seen, f"duplicate target {key}")
        seen.add(key)
        require("expected_value" in cell and cell.get("basis") and cell.get("review_range"), "observed cell/header context required")
        require(type(cell.get("overwrite_existing", False)) is bool, "invalid overwrite flag")
        require(isinstance(cell.get("identity"), dict) and cell["identity"].get("uc_id") == requested_uc,
                "cell outside requested UC")
        update = dict(cell, value="N/A", reason=None, source=None, source_sha256=None)
        try:
            identity = cell.get("identity", {})
            require(identity and set(identity) <= IDENTITY and "uc_id" in identity, "unresolved/invalid run identity")
            invalid_candidates = [item for item in errors if item["uc_id"] == identity["uc_id"]
                                  and ("run_id" not in identity or item["run_id"] == identity["run_id"])]
            require(not invalid_candidates, "candidate source unavailable: " +
                    "; ".join(item["reason"] for item in invalid_candidates))
            matches = []
            for source, checksum, record in sources:
                try:
                    match = all(lookup(record, k) == v for k, v in identity.items())
                except ValueError:
                    match = False
                if match:
                    matches.append((source, checksum, record))
            require(len(matches) == 1, f"expected one source record, found {len(matches)}")
            source, checksum, record = matches[0]
            update.update(source=source, source_sha256=checksum)
            require(cell.get("field") is not None, cell.get("unresolved_reason") or "metric/units ambiguous")
            if cell.get("source_unit") is not None:
                require(cell.get("semantic_reason"), "explicit source unit requires semantic evidence")
            update["value"] = resolve_value(record, cell["field"], cell.get("type"), cell.get("conversion", "identity"), cell.get("source_unit"))
        except (ValueError, KeyError, TypeError, IndexError, AttributeError, ArithmeticError) as error:
            update["reason"] = str(error)
        updates.append(update)
    return {"schema_version": 1, "export_mode": export_mode,
            "requested_uc_id": requested_uc, "target_sheet": target_sheet,
            "target_reference": mapping.get("target_reference"), "header_coverage": mapping.get("header_coverage", []),
            "repo_root": str(ROOT), "workbook": str(workbook),
            "workbook_sha256": mapping["workbook_sha256"], "updates": updates,
            "issues": mapping.get("issues", []), "source_errors": errors,
            "filled_count": sum(u["reason"] is None for u in updates),
            "na_count": sum(u["reason"] is not None for u in updates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = prepare(read_json(args.mapping))
    if args.output:
        atomic_write(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
