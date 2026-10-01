#!/usr/bin/env python3
"""Validate one completed experiment configuration and print its SHA-256 pin.

This researcher-side helper is read-only. It does not update the configuration
or the Canonical Run JSON that will pin the printed checksum.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".codex/scripts"))
from validate_experiment_configuration import validate  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configuration", required=True, type=Path,
                        help="Completed Confirmed experiment configuration JSON")
    args = parser.parse_args()

    path = (args.configuration if args.configuration.is_absolute()
            else ROOT / args.configuration).resolve()
    raw = path.read_bytes()
    configuration = validate(path)
    if path.read_bytes() != raw:
        raise ValueError("configuration changed during validation")
    artifact = path.relative_to(ROOT).as_posix()
    output = {
        "experiment_configuration": {
            "configuration_id": configuration["configuration_id"],
            "artifact": artifact,
            "checksum": "sha256:" + hashlib.sha256(raw).hexdigest(),
        }
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"configuration checksum calculation blocked: {exc}")
