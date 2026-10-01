#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from resolve import DATASET_ROOT, verify


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-freeze one checksum-valid, plugin-validated Figma node")
    parser.add_argument("--source", required=True)
    parser.add_argument("--new-version", required=True)
    parser.add_argument("--uc-id", required=True)
    parser.add_argument("--plugin-file-key", required=True)
    parser.add_argument("--plugin-node-id", required=True)
    parser.add_argument("--plugin-frame-name", required=True)
    parser.add_argument("--plugin-width", required=True, type=int)
    parser.add_argument("--plugin-height", required=True, type=int)
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{3}", args.new_version):
        raise SystemExit("new-version must have the format YYYY-MM-DD-NNN")

    source = DATASET_ROOT / args.source
    destination = DATASET_ROOT / args.new_version
    if not (source / "manifest.json").is_file():
        raise SystemExit(f"Source dataset does not exist: {args.source}")
    if destination.exists():
        raise SystemExit(f"Destination dataset already exists: {args.new_version}")

    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    uc_id = f"UC-{int(re.search(r'\d+', args.uc_id).group()):03d}"
    uc_entry = manifest.get("use_cases", {}).get(uc_id)
    node = manifest.get("nodes", {}).get(args.plugin_node_id)
    if not uc_entry or uc_entry.get("node_id") != args.plugin_node_id or not node:
        raise SystemExit("UC/node does not match the source manifest")
    if (
        node.get("file_key") != args.plugin_file_key
        or node.get("frame_name") != args.plugin_frame_name
    ):
        raise SystemExit("Plugin metadata does not match the file key/frame in the source manifest")

    checks = verify(source)
    node_prefix = f"nodes/{args.plugin_node_id.replace(':', '-')}/"
    node_checks = [item for item in checks if item["path"].startswith(node_prefix)]
    node_failures = [item for item in node_checks if not item["ok"]]
    if not node_checks:
        raise SystemExit("Checksum ledger does not contain the target node payload")
    if node_failures:
        raise SystemExit(json.dumps({"status": "source-integrity-failed", "files": node_failures}, ensure_ascii=False, indent=2))

    with tempfile.TemporaryDirectory(prefix="figma-refreeze-", dir=DATASET_ROOT) as temporary:
        staged = Path(temporary) / args.new_version
        staged.mkdir()
        snapshot_relative = Path(node["snapshot_dir"])
        shutil.copytree(source / snapshot_relative, staged / snapshot_relative)

        manifest_path = staged / "manifest.json"
        original_created_at = manifest.get("created_at")
        refrozen_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        manifest["dataset_id"] = args.new_version
        manifest["dataset_version"] = args.new_version
        manifest["created_at"] = refrozen_at
        manifest["overall_status"] = "partial-content"
        manifest["complete_nodes"] = 1
        manifest["partial_content_nodes"] = sum(1 for item in manifest["nodes"].values() if item is not node)
        manifest["refrozen_at"] = refrozen_at
        manifest["derived_from_dataset"] = args.source
        manifest["source_capture_created_at"] = original_created_at
        manifest["refreeze_scope"] = [uc_id]
        manifest["refreeze_reason"] = "Portable checksum ledger for one checksum-valid node after Git newline normalization."
        manifest["plugin_validation"] = {
            "validated_at": refrozen_at,
            "file_key": args.plugin_file_key,
            "node_id": args.plugin_node_id,
            "frame_name": args.plugin_frame_name,
            "width": args.plugin_width,
            "height": args.plugin_height,
        }
        for node_id, item in manifest["nodes"].items():
            if node_id == args.plugin_node_id:
                item["status"] = "complete"
                continue
            item["snapshot_dir"] = None
            item["status"] = "partial-content"
            item["missing_reason"] = "not_in_focused_refreeze"
        for item in manifest["use_cases"].values():
            if item.get("node_id") is None:
                continue
            item["status"] = "complete" if item["node_id"] == args.plugin_node_id else "partial-content"

        metadata_path = staged / snapshot_relative / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("natural_width") != args.plugin_width or metadata.get("natural_height") != args.plugin_height:
            raise SystemExit("Plugin dimensions do not match the metadata payload")
        metadata["dataset_version"] = args.new_version
        metadata["source_dataset_version"] = args.source
        metadata["plugin_validated_at"] = refrozen_at
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

        checksum_path = staged / "checksums.sha256"
        data_files = sorted(path for path in staged.rglob("*") if path.is_file() and path != checksum_path)
        lines = [f"{digest(path)}  {path.relative_to(staged).as_posix()}" for path in data_files]
        checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        staged.rename(destination)

    print(json.dumps({
        "status": "refrozen",
        "source_dataset": args.source,
        "dataset_id": args.new_version,
        "uc_id": uc_id,
        "node_id": args.plugin_node_id,
        "payload_files_verified": len(node_checks),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
