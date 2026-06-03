from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "report": args.report,
        "receipt": args.receipt,
        "raw_dicom_packaged": False,
        "boundary": "delivery package excludes original DICOM",
    }
    (out_dir / "delivery_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(out_dir / "delivery_manifest.json")


if __name__ == "__main__":
    main()
