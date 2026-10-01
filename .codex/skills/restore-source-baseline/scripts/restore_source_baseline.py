#!/usr/bin/env python3
"""Safely restore finalsource/{be,fe}/src from the bundled baseline asset."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


CONFIRMATION = "RESET_FINALSOURCE_TO_PROVIDED_BASELINE"
ALLOWED_PREFIXES = ("baseline/be/src/", "baseline/fe/src/")
DATABASE_INFRASTRUCTURE = ("database/migrations", "database/migration-data-source.ts", "config/database.config.ts")


def fail(message: str) -> None:
    raise SystemExit(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_digest(root: Path) -> tuple[str | None, int]:
    if not root.is_dir():
        return None, 0
    digest = hashlib.sha256()
    count = 0
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
        count += 1
    return digest.hexdigest(), count


def profile_asset_sha256(repo: Path) -> str:
    profile_path = repo / "PROJECT_PROFILE.json"
    if not profile_path.is_file():
        fail("PROJECT_PROFILE.json is missing")
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"PROJECT_PROFILE.json is invalid JSON: {error}")
    value = profile.get("clean_source_baseline_sha256") if isinstance(profile, dict) else None
    if not isinstance(value, str) or not value.startswith("sha256:"):
        fail("PROJECT_PROFILE.json clean_source_baseline_sha256 must use sha256:<64 lowercase hex>")
    checksum = value.removeprefix("sha256:")
    if len(checksum) != 64 or any(character not in "0123456789abcdef" for character in checksum):
        fail("PROJECT_PROFILE.json clean_source_baseline_sha256 must use sha256:<64 lowercase hex>")
    return checksum


def validate_archive(archive: Path, expected_sha256: str) -> None:
    if sha256_file(archive) != expected_sha256:
        fail("baseline asset checksum does not match PROJECT_PROFILE.json")
    with zipfile.ZipFile(archive) as bundle:
        files = []
        for entry in bundle.infolist():
            name = entry.filename
            parts = PurePosixPath(name).parts
            if name.startswith("/") or ".." in parts:
                fail(f"unsafe archive entry: {name}")
            if entry.is_dir():
                continue
            if not name.startswith(ALLOWED_PREFIXES):
                fail(f"unexpected archive entry: {name}")
            mode = entry.external_attr >> 16
            if mode & 0o170000 == 0o120000:
                fail(f"symbolic links are not allowed: {name}")
            files.append(name)
        if not files or not any(name.startswith("baseline/be/src/") for name in files):
            fail("backend baseline source is missing")
        if not any(name.startswith("baseline/fe/src/") for name in files):
            fail("frontend baseline source is missing")


def extract_archive(archive: Path, destination: Path, expected_sha256: str) -> None:
    validate_archive(archive, expected_sha256)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(destination)


def preserve_database_infrastructure(current: Path, baseline: Path) -> None:
    """Overlay researcher-owned database files on the temporary source baseline."""
    for relative in DATABASE_INFRASTRUCTURE:
        source = current / relative
        if not source.exists():
            fail(f"missing database infrastructure: {relative}; prepare it before source restoration")
        paths = [source, *source.rglob("*")] if source.is_dir() else [source]
        if any(path.is_symlink() or not path.resolve().is_relative_to(current.resolve()) for path in paths):
            fail(f"unsafe database infrastructure: {relative}")
        destination = baseline / relative
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def make_backup(targets: dict[str, Path], backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = backup_dir / f"before-baseline-restore-{timestamp}.zip"
    if backup.exists():
        fail(f"backup already exists: {backup}")
    with zipfile.ZipFile(backup, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for label, root in targets.items():
            if not root.is_dir():
                continue
            for path in sorted(item for item in root.rglob("*") if item.is_file()):
                bundle.write(path, f"{label}/{path.relative_to(root).as_posix()}")
    return backup


def restore_backup(backup: Path, targets: dict[str, Path]) -> None:
    for target in targets.values():
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
    with zipfile.ZipFile(backup) as bundle:
        for entry in bundle.infolist():
            if entry.is_dir():
                continue
            label, _, relative = entry.filename.partition("/")
            if label not in targets or not relative:
                fail(f"invalid backup entry: {entry.filename}")
            destination = targets[label] / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(entry) as source, destination.open("wb") as output:
                shutil.copyfileobj(source, output)


def summary(targets: dict[str, Path], baseline: dict[str, Path]) -> dict[str, object]:
    result: dict[str, object] = {}
    for label in targets:
        current_hash, current_files = tree_digest(targets[label])
        baseline_hash, baseline_files = tree_digest(baseline[label])
        result[label] = {
            "current_tree_sha256": current_hash,
            "current_files": current_files,
            "baseline_tree_sha256": baseline_hash,
            "baseline_files": baseline_files,
            "matches_baseline": current_hash == baseline_hash,
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()

    script = Path(__file__).resolve()
    repo = script.parents[4]
    if not (repo / "PROJECT_CONTEXT.md").is_file() or not (repo / "finalsource").is_dir():
        fail("repository identity check failed")

    skill = script.parents[1]
    archive = skill / "assets" / "source-baseline.zip"
    if not archive.is_file():
        fail("baseline asset is missing")
    expected_asset_sha256 = profile_asset_sha256(repo)

    targets = {
        "be": repo / "finalsource" / "be" / "src",
        "fe": repo / "finalsource" / "fe" / "src",
    }
    for path in (repo / "finalsource", repo / "finalsource" / "be", repo / "finalsource" / "fe", *targets.values()):
        if path.is_symlink():
            fail(f"refusing symbolic-link target: {path}")

    with tempfile.TemporaryDirectory(prefix="baseline-check-") as temporary:
        extracted = Path(temporary)
        extract_archive(archive, extracted, expected_asset_sha256)
        baseline = {
            "be": extracted / "baseline" / "be" / "src",
            "fe": extracted / "baseline" / "fe" / "src",
        }
        preserve_database_infrastructure(targets["be"], baseline["be"])
        before = summary(targets, baseline)
        if args.check:
            print(json.dumps({"mode": "check", "targets": before}, indent=2))
            return 0

        if args.confirm != CONFIRMATION:
            fail(f"apply requires --confirm {CONFIRMATION}")

        backup = make_backup(targets, repo / ".tmp" / "source-baseline-backups")
        try:
            for label, target in targets.items():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(baseline[label], target)
            after = summary(targets, baseline)
            if not all(item["matches_baseline"] for item in after.values()):
                raise RuntimeError("post-restore hash verification failed")
        except Exception:
            restore_backup(backup, targets)
            raise

    print(
        json.dumps(
            {
                "mode": "apply",
                "backup": str(backup.relative_to(repo)),
                "targets": after,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, zipfile.BadZipFile) as error:
        print(f"restore failed: {error}", file=sys.stderr)
        raise SystemExit(1)
