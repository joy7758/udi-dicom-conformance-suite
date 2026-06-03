from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-folder", required=True)
    parser.add_argument("--validator-command", default="udi-dicom-validate")
    parser.add_argument("--out", default="batch_summary.json")
    args = parser.parse_args()
    sample_folder = Path(args.sample_folder)
    if not sample_folder.exists():
        raise SystemExit(f"sample folder not found: {sample_folder}")
    summary = {
        "sample_folder": str(sample_folder),
        "validator_command": args.validator_command,
        "status": "planned",
        "receipts": [],
    }
    Path(args.out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(args.out)


if __name__ == "__main__":
    main()
