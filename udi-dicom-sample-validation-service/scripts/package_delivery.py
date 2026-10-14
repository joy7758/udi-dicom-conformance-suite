from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--profile-version", default="v0.2.0")
    parser.add_argument("--private-suite-version", default="v0.2.0")
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "report": args.report,
        "receipt": args.receipt,
        "profile_version": args.profile_version,
        "private_suite_version": args.private_suite_version,
        "delivery_manifest_version": "v0.2",
        "supports_trace_id": True,
        "supports_fdo_mapping": True,
        "raw_dicom_packaged": False,
        "boundary": "delivery package excludes original DICOM",
    }
    output = out_dir / "delivery_manifest_v0.2.json"
    output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(output)


if __name__ == "__main__":
    main()
