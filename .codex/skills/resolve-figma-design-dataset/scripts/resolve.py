#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Optional


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "PROJECT_CONTEXT.md").is_file():
            return parent
    raise SystemExit("Cannot find the repository root containing PROJECT_CONTEXT.md")


ROOT = repo_root()
DATASET_ROOT = ROOT / "resource/figma-design-dataset"


def select_dataset(version: str) -> Path:
    if version in {".", ".."} or not re.fullmatch(r"[A-Za-z0-9._-]+", version):
        raise FileNotFoundError("Dataset version must be a safe directory name")
    candidate = (DATASET_ROOT / version).resolve()
    if not candidate.is_relative_to(DATASET_ROOT.resolve()) or not (candidate / "manifest.json").is_file():
        raise FileNotFoundError(f"Dataset version does not exist or is missing a manifest: {version}")
    return candidate


def normalize_uc(value: str) -> str:
    match = re.search(r"(?i)uc[-_ ]*0*(\d{1,3})", value)
    if not match:
        raise ValueError(f"Cannot identify the UC from: {value}")
    return f"UC-{int(match.group(1)):03d}"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def crlf_digest(path: Path) -> Optional[str]:
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    canonical_lf = text.replace("\r\n", "\n").replace("\r", "\n")
    canonical_crlf = canonical_lf.replace("\n", "\r\n").encode("utf-8")
    return hashlib.sha256(canonical_crlf).hexdigest()


def verify(dataset: Path) -> list[dict]:
    results = []
    for line in (dataset / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        # Checksum ledgers may be created on Windows and retained as immutable
        # evidence. Resolve their separators portably without rewriting them.
        normalized_relative = relative.replace("\\", "/")
        relative_path = Path(normalized_relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Unsafe checksum path: {relative}")
        target = dataset.joinpath(*relative_path.parts)
        actual = digest(target) if target.is_file() else None
        matched_via = "raw-bytes" if actual == expected else None
        if target.is_file() and matched_via is None and crlf_digest(target) == expected:
            matched_via = "canonical-crlf"
        results.append({
            "path": normalized_relative,
            "ok": matched_via is not None,
            "expected": expected,
            "actual": actual,
            "matched_via": matched_via,
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve immutable UC to frozen Figma dataset")
    parser.add_argument("target", nargs="?", help="UC ID or UC file path")
    parser.add_argument("--validate-all", action="store_true")
    parser.add_argument("--dataset-version", required=True,
                        help="Exact immutable dataset directory name to use")
    args = parser.parse_args()
    try:
        dataset = select_dataset(args.dataset_version)
    except FileNotFoundError as error:
        print(json.dumps({"status": "no-dataset", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 4
    manifest = json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))
    try:
        checks = verify(dataset)
    except (ValueError, OSError) as error:
        print(json.dumps({"status": "invalid-checksum-ledger", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    integrity_ok = all(item["ok"] for item in checks)
    if args.validate_all:
        print(json.dumps({"dataset_id": manifest["dataset_id"], "integrity_ok": integrity_ok, "files": checks}, ensure_ascii=False, indent=2))
        return 0 if integrity_ok else 2
    if not args.target:
        parser.error("target or --validate-all is required")
    try:
        key = normalize_uc(args.target)
    except ValueError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    entry = manifest["use_cases"].get(key)
    if entry is None:
        print(json.dumps({"error": f"{key} is not in the manifest"}, ensure_ascii=False), file=sys.stderr)
        return 2
    node = manifest["nodes"].get(entry["node_id"]) if entry["node_id"] else None
    output = {"uc_id": key, "status": entry["status"], "dataset_id": manifest["dataset_id"], "node_id": entry["node_id"], "integrity_ok": integrity_ok}
    if node:
        output.update({"frame_name": node["frame_name"], "snapshot_dir": str(dataset / node["snapshot_dir"]) if node["snapshot_dir"] else None})
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if entry["status"] in {"complete", "no-design"} and integrity_ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
