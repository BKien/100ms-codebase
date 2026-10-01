#!/usr/bin/env python3
"""Read-only validation of prompt identity, structure and activation links."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "measure-uc-workflow/scripts"))
from metrics_contract import ROOT, digest, read_json, require, writable, epoch
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from validate_experiment_configuration import validate as validate_configuration, identifier


def normalize_variant(value):
    normalized = identifier(value, "prompt_variant")
    require(value == normalized, "prompt_variant must be a canonical identifier")
    return normalized


def prompt_metadata(path):
    content = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
    require(match is not None, "prompt needs scalar YAML frontmatter")
    metadata = {}
    for line in match[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        field = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
        require(field is not None and field[1] not in metadata, "invalid/duplicate prompt metadata")
        value = field[2]
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        metadata[field[1]] = value
    # Ignore fenced examples when identifying actual prompt sections.
    body = content[match.end():]
    visible, fence = [], None
    for line in body.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            continue
        if fence is None:
            visible.append(line)
    headings = re.findall(r"^##\s+Prompt\s+([A-Z])\s*:", "\n".join(visible), re.M)
    return metadata, body, headings


def configured_headings():
    template = writable(ROOT / "templates/construction/coding-prompt.template.md")
    require(template.is_file(), "configured coding prompt template missing")
    _, _, headings = prompt_metadata(template)
    require(headings and len(headings) == len(set(headings)),
            "configured coding prompt template has invalid prompt sections")
    return headings


def configured_api_metadata(uc):
    contracts = uc.get("api_contracts")
    require(isinstance(contracts, list) and contracts, "configured API contracts missing")
    return ";".join(entry["path"] for entry in contracts)


def validate_prompt(configuration, uc_id, run_id, prompt, activation=None, allow_draft=False):
    configuration, prompt = writable(configuration), writable(prompt)
    config = validate_configuration(configuration)
    assignments = [r for r in config["runs"] if r.get("uc_id") == uc_id and r.get("run_id") == run_id]
    require(len(assignments) == 1, "prompt needs unique configured UC/run")
    variant = normalize_variant(assignments[0].get("prompt_variant"))
    meta, body, headings = prompt_metadata(prompt)
    require(meta.get("artifact_type") == "business-coding-prompt" and meta.get("uc_id") == uc_id, "prompt UC/type mismatch")
    require(meta.get("status") in ({"Draft", "Approved"} if allow_draft else {"Approved"}), "prompt approval status mismatch")
    actual = normalize_variant(meta.get("prompt_variant"))
    require(actual == variant, "configuration/prompt variant mismatch")
    require(headings == configured_headings(), "prompt sections must match configured template exactly")
    require(prompt.name.endswith("-business-coding-prompt.md"), "prompt filename/variant mismatch")
    uc = config["use_case"]
    require(uc.get("uc_id") == uc_id, "configuration/prompt UC mismatch")
    baseline = read_json(writable(ROOT / uc["business_rule_baseline"]))
    require(baseline.get("status") == "Frozen" and baseline.get("uc_id") == uc_id, "BR baseline identity mismatch")
    require(meta.get("source_use_case") == baseline.get("use_case_path"), "prompt source UC mismatch")
    require(meta.get("source_api_contracts") == configured_api_metadata(uc),
            "prompt source API contracts mismatch")
    require(meta.get("business_rule_baseline") == uc["business_rule_baseline"], "BR baseline reference mismatch")
    reference = {"path": prompt.relative_to(ROOT).as_posix(), "sha256": digest(prompt.read_bytes())}
    if activation is not None:
        receipt = read_json(writable(activation))
        require(receipt.get("status") == "Confirmed" and receipt.get("artifact_type") == "run-activation", "invalid activation")
        require(type(receipt.get("gate_version")) is int and receipt["gate_version"] == 5, "invalid activation gate version")
        epoch(receipt.get("activated_at"))
        require(receipt.get("uc_id") == uc_id and receipt.get("run_id") == run_id, "activation UC/run mismatch")
        require(normalize_variant(receipt.get("prompt_variant")) == variant, "activation/prompt variant mismatch")
        require(receipt.get("configuration_artifact") == configuration.relative_to(ROOT).as_posix()
                and receipt.get("configuration_checksum") == digest(configuration.read_bytes()), "activation configuration mismatch")
        require(receipt.get("approved_prompt") == reference, "activated prompt is immutable")
    return {"status": "valid", "uc_id": uc_id, "run_id": run_id, "prompt_variant": variant, "prompt": reference}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configuration", required=True, type=Path)
    parser.add_argument("--uc-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--activation", type=Path)
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate_prompt(args.configuration, args.uc_id, args.run_id, args.prompt,
                                     args.activation, args.allow_draft), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"prompt contract error: {exc}")
