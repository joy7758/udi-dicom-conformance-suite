from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-folder", required=True)
    parser.add_argument("--validator-command", default="udi-dicom-validate")
    parser.add_argument("--profile-version", default="v0.2.0")
    parser.add_argument("--private-suite-version", default="v0.2.0")
    parser.add_argument("--private-suite-path")
    parser.add_argument("--out", default="batch_summary_v0.2.json")
    args = parser.parse_args()
    sample_folder = Path(args.sample_folder)
    if not sample_folder.exists():
        raise SystemExit(f"sample folder not found: {sample_folder}")
    if args.private_suite_path and not Path(args.private_suite_path).exists():
        raise SystemExit(f"private suite path not found: {args.private_suite_path}")
    summary = {
        "sample_folder": str(sample_folder),
        "validator_command": args.validator_command,
        "profile_version": args.profile_version,
        "private_suite_version": args.private_suite_version,
        "private_suite_path": args.private_suite_path,
        "batch_summary_version": "v0.2",
        "supports_trace_id": True,
        "supports_fdo_mapping": True,
        "redact_check_required": True,
        "status": "planned",
        "receipts": [],
    }
    Path(args.out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(args.out)


if __name__ == "__main__":
    main()
