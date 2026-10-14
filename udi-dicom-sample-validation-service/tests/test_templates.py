from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_templates_exist_and_contain_boundaries() -> None:
    required = [
        ROOT / "reports/templates/sample-validation-report.md",
        ROOT / "reports/templates/executive-summary.md",
        ROOT / "service-offering.md",
    ]
    for path in required:
        text = path.read_text(encoding="utf-8")
        assert "not clinical validation" in text
        assert "not regulatory approval" in text
        assert "no PHI" in text
        assert "not certification" in text


def test_v02_batch_and_delivery_scripts(tmp_path: Path) -> None:
    sample_folder = ROOT / "reports" / "examples"
    batch = tmp_path / "batch_summary_v0.2.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_validation_batch.py"),
            "--sample-folder",
            str(sample_folder),
            "--out",
            str(batch),
        ],
        check=True,
    )
    data = json.loads(batch.read_text(encoding="utf-8"))
    assert data["profile_version"] == "v0.2.0"
    assert data["supports_trace_id"] is True
    out_dir = tmp_path / "delivery"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "package_delivery.py"),
            "--report",
            str(ROOT / "reports" / "examples" / "synthetic-report-example.md"),
            "--receipt",
            str(batch),
            "--out-dir",
            str(out_dir),
        ],
        check=True,
    )
    delivery = json.loads((out_dir / "delivery_manifest_v0.2.json").read_text())
    assert delivery["delivery_manifest_version"] == "v0.2"
    assert delivery["raw_dicom_packaged"] is False
