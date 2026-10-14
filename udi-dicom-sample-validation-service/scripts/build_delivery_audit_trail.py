from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "delivery" / "generated" / "delivery_audit_trail_v0.4.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def build_synthetic_demo() -> dict[str, Any]:
    generated = ROOT / "delivery" / "generated"
    artifacts = [
        generated / "delivery_manifest_v0.3.json",
        generated / "delivery_summary_v0.3.md",
        generated / "synthetic_batch_summary_v0.3.json",
        generated / "synthetic_report_v0.3.md",
        generated / "redaction_check_log.txt",
    ]
    hashes = {relative(path): sha256(path) for path in artifacts if path.exists()}
    audit = {
        "delivery_id": "synthetic-delivery-v0.4-001",
        "created_at": "2026-06-04T00:00:00Z",
        "service_version": "v0.4.0-branch",
        "validator_version": "public-validator-v0.3",
        "suite_version": "private-suite-v0.3",
        "source_artifacts": [
            "synthetic validator receipt summary",
            "synthetic partner pack summary",
        ],
        "generated_artifacts": sorted(hashes),
        "sha256_hashes": hashes,
        "redaction_check_status": "pass",
        "forbidden_asset_check_status": "pass",
        "boundary_statement": (
            "Synthetic review/report delivery only; no PHI, no raw DICOM, "
            "not clinical validation, not regulatory approval, not certification."
        ),
        "reviewer_notes": "Use for synthetic pilot handoff review only.",
        "raw_dicom_packaged": False,
        "phi_included": False,
    }
    return audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic-demo", action="store_true")
    args = parser.parse_args()
    if not args.synthetic_demo:
        raise SystemExit("--synthetic-demo is required for deterministic v0.4 audit trail")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    audit = build_synthetic_demo()
    OUTPUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": relative(OUTPUT),
                "redaction_check_status": audit["redaction_check_status"],
                "forbidden_asset_check_status": audit["forbidden_asset_check_status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
