from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_pilot_e2e_outputs_are_safe() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "run_synthetic_pilot_e2e.py")], check=True)
    out = ROOT / "artifacts" / "synthetic-pilot-e2e"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_synthetic_pilot_outputs.py"), str(out)],
        check=True,
    )
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["raw_dicom_copied"] is False
    assert summary["phi_included"] is False
    assert summary["redaction_check_status"] == "pass"
    assert summary["delivery_package_check_status"] == "pass"
