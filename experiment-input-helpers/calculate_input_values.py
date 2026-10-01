#!/usr/bin/env python3
"""Print objective experiment input paths, identities and SHA-256 pins.

This researcher-side helper is read-only. It does not create or update any
configuration, baseline, Canonical Run JSON, database object or Figma dataset.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
API_ROOT = (ROOT / "docs/01-inception/api-contracts").resolve()
UC_ROOT = (ROOT / "docs/01-inception/use-cases").resolve()
FIGMA_ROOT = (ROOT / "resource/figma-design-dataset").resolve()
BASELINE_ARCHIVE = ".codex/skills/restore-source-baseline/assets/source-baseline.zip"

sys.path.insert(0, str(ROOT / ".codex/skills/gen-coding-prompt/scripts"))
from database_baseline import capture as capture_database  # noqa: E402
from database_baseline import dbml_file  # noqa: E402


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(raw):
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def repository_file(value, root, suffix, label):
    supplied = Path(value)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).resolve()
    require(path.is_relative_to(root), f"{label} must stay under {root.relative_to(ROOT).as_posix()}")
    require(path.suffix.lower() == suffix, f"{label} must be a {suffix} file")
    require(path.is_file(), f"{label} does not exist: {value}")
    return path


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def frontmatter(content, label):
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.S)
    require(match is not None, f"{label} frontmatter missing")
    metadata = {}
    for line in match.group(1).splitlines():
        item = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
        if item:
            key, value = item.groups()
            require(key not in metadata, f"duplicate {label} frontmatter field: {key}")
            metadata[key] = value.strip().strip('"').strip("'")
    return metadata


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


def inspect_use_case(value):
    path = repository_file(value, UC_ROOT, ".md", "use case")
    raw = path.read_bytes()
    metadata = frontmatter(raw.decode("utf-8-sig"), "use case")
    require(metadata.get("artifact_type") == "business-use-case-specification",
            "use case artifact_type must be business-use-case-specification")
    require(metadata.get("status") == "Frozen", "use case status must be Frozen")
    uc_id = metadata.get("uc_id")
    require(isinstance(uc_id, str) and re.fullmatch(r"UC-[A-Za-z0-9_-]+", uc_id),
            "use case uc_id is missing or invalid")
    return path, raw, uc_id, source_api_ids(raw)


def inspect_api_contract(value, expected_id):
    path = repository_file(value, API_ROOT, ".md", "API contract")
    raw = path.read_bytes()
    metadata = frontmatter(raw.decode("utf-8-sig"), "API contract")
    require(metadata.get("artifact_type") == "api-contract", "API contract artifact_type must be api-contract")
    require(metadata.get("status") == "Frozen", "API contract status must be Frozen")
    require(metadata.get("api_id") == expected_id,
            f"API contract identity/order mismatch: expected {expected_id}, got {metadata.get('api_id')}")
    return {"api_id": expected_id, "path": relative(path), "sha256": sha256(raw)}, path, raw


def inspect_figma_dataset(version):
    require(isinstance(version, str) and version not in {"", ".", ".."}
            and re.fullmatch(r"[A-Za-z0-9._-]+", version), "invalid Figma dataset version")
    manifest = (FIGMA_ROOT / version / "manifest.json").resolve()
    require(manifest.is_relative_to(FIGMA_ROOT) and manifest.is_file(),
            f"Figma dataset manifest does not exist for version: {version}")
    raw = manifest.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object)
    require(isinstance(data, dict), "Figma manifest must be a JSON object")
    require(data.get("dataset_version") == version, "Figma manifest dataset_version mismatch")
    require(data.get("overall_status") == "complete", "Figma dataset must be complete")
    return {
        "dataset_version": version,
        "manifest_path": relative(manifest),
        "manifest_sha256": sha256(raw),
    }, manifest, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--use-case", required=True, help="Frozen repository UC Markdown path")
    parser.add_argument("--api-contract", action="append", required=True,
                        help="Frozen API Markdown path; repeat in the UC's Related API IDs order")
    parser.add_argument("--figma-dataset-version", required=True,
                        help="Exact immutable Figma dataset directory name")
    parser.add_argument("--require-empty", action="store_true",
                        help="Pipeline initialization only: require application tables to be empty")
    args = parser.parse_args()

    uc_path, uc_raw, uc_id, expected_api_ids = inspect_use_case(args.use_case)
    require(len(args.api_contract) == len(expected_api_ids),
            f"expected {len(expected_api_ids)} --api-contract argument(s) in this order: {', '.join(expected_api_ids)}")

    api_contracts = []
    api_snapshots = []
    seen_paths = set()
    for supplied, expected_id in zip(args.api_contract, expected_api_ids):
        entry, path, raw = inspect_api_contract(supplied, expected_id)
        require(entry["path"] not in seen_paths, f"duplicate API contract path: {entry['path']}")
        seen_paths.add(entry["path"])
        api_contracts.append(entry)
        api_snapshots.append((path, raw))

    figma, manifest_path, manifest_raw = inspect_figma_dataset(args.figma_dataset_version)

    archive_path = (ROOT / BASELINE_ARCHIVE).resolve()
    require(archive_path.is_relative_to(ROOT) and archive_path.is_file(), "clean source baseline ZIP is missing")
    archive_raw = archive_path.read_bytes()

    _, dbml_checksum = dbml_file()
    migration_head, schema_fingerprint = capture_database(require_empty=args.require_empty)
    require(dbml_file()[1] == dbml_checksum, "DBML changed during database fingerprint capture")

    require(uc_path.read_bytes() == uc_raw, "use case changed during input calculation")
    require(all(path.read_bytes() == raw for path, raw in api_snapshots),
            "an API contract changed during input calculation")
    require(manifest_path.read_bytes() == manifest_raw, "Figma manifest changed during input calculation")
    require(archive_path.read_bytes() == archive_raw, "clean source baseline changed during input calculation")

    uc_relative = relative(uc_path)
    uc_checksum = sha256(uc_raw)
    implementation_root = f"docs/02-construction/implementation/{uc_id}"
    output = {
        "clean_source_baseline": {
            "path": BASELINE_ARCHIVE,
            "clean_source_baseline_sha256": sha256(archive_raw),
        },
        "use_case": {
            "uc_id": uc_id,
            "path": uc_relative,
            "sha256": uc_checksum,
        },
        "baseline_values": {
            "business_rule_baseline": {
                "path": f"{implementation_root}/business-rule-baseline.json",
                "use_case_path": uc_relative,
                "use_case_sha256": uc_checksum,
            },
            "flow_baseline": {
                "path": f"{implementation_root}/flow-baseline.json",
                "use_case_path": uc_relative,
                "use_case_sha256": uc_checksum,
            },
        },
        "api_contracts": api_contracts,
        "database_baseline": {
            "migration_head": migration_head,
            "dbml_sha256": dbml_checksum,
            "schema_fingerprint_sha256": schema_fingerprint,
        },
        "figma_dataset": figma,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"experiment input calculation blocked: {exc}")
