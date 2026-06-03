from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "delivery" / "generated"


def synthetic_inputs() -> dict[str, str]:
    sample_batch = {
        "batch_summary_version": "v0.3",
        "profile_version": "v0.2.0",
        "receipt_count": 0,
        "redact_check_required": True,
        "raw_dicom_packaged": False,
    }
    GENERATED.mkdir(parents=True, exist_ok=True)
    batch = GENERATED / "synthetic_batch_summary_v0.3.json"
    report = GENERATED / "synthetic_report_v0.3.md"
    redaction = GENERATED / "redaction_check_log.txt"
    batch.write_text(json.dumps(sample_batch, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report.write_text(
        "# Synthetic Delivery Report\n\nNo PHI. Not clinical validation. Not regulatory approval.\n",
        encoding="utf-8",
    )
    redaction.write_text("redact_check=pass\n", encoding="utf-8")
    return {"batch_summary": str(batch), "report": str(report), "redaction_log": str(redaction)}


def build_package(batch_summary: Path, report: Path, redaction_log: Path) -> dict[str, object]:
    for path in [batch_summary, report, redaction_log]:
        if not path.exists():
            raise SystemExit(f"input not found: {path}")
    GENERATED.mkdir(parents=True, exist_ok=True)
    manifest = {
        "delivery_manifest_version": "v0.3",
        "batch_summary": str(batch_summary),
        "report": str(report),
        "redaction_log": str(redaction_log),
        "raw_dicom_packaged": False,
        "forbidden_artifacts_packaged": False,
        "allowed_outputs": [
            "delivery_manifest_v0.3.json",
            "delivery_summary_v0.3.md",
            "receipt summaries",
            "redaction check log",
        ],
        "forbidden_outputs": [
            "original DICOM files",
            "patient report",
            "raw clinical report",
            "private conformance cases",
            "customer confidential artifacts",
        ],
        "boundary": [
            "no PHI",
            "not clinical validation",
            "not regulatory approval",
            "not certification",
        ],
    }
    (GENERATED / "delivery_manifest_v0.3.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (GENERATED / "delivery_summary_v0.3.md").write_text(
        "# Delivery Summary v0.3\n\n"
        "Generated delivery package excludes original DICOM, patient reports, "
        "raw clinical reports, private conformance cases, and customer confidential artifacts.\n\n"
        "Boundary: no PHI, not clinical validation, not regulatory approval, not certification.\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-summary")
    parser.add_argument("--report")
    parser.add_argument("--redaction-log")
    parser.add_argument("--synthetic-demo", action="store_true")
    args = parser.parse_args()
    if args.synthetic_demo:
        paths = synthetic_inputs()
        batch_summary = Path(paths["batch_summary"])
        report = Path(paths["report"])
        redaction_log = Path(paths["redaction_log"])
    else:
        if not (args.batch_summary and args.report and args.redaction_log):
            raise SystemExit("--batch-summary, --report, and --redaction-log are required")
        batch_summary = Path(args.batch_summary)
        report = Path(args.report)
        redaction_log = Path(args.redaction_log)
    manifest = build_package(batch_summary, report, redaction_log)
    print(json.dumps({"generated": True, "raw_dicom_packaged": manifest["raw_dicom_packaged"]}, sort_keys=True))


if __name__ == "__main__":
    main()
