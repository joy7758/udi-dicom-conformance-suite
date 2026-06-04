from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_delivery_audit_trail_synthetic_demo() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_delivery_package.py"), "--synthetic-demo"],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_delivery_audit_trail.py"), "--synthetic-demo"],
        check=True,
    )
    audit = json.loads(
        (ROOT / "delivery" / "generated" / "delivery_audit_trail_v0.4.json").read_text()
    )
    assert audit["delivery_id"] == "synthetic-delivery-v0.4-001"
    assert audit["redaction_check_status"] == "pass"
    assert audit["forbidden_asset_check_status"] == "pass"
    assert audit["raw_dicom_packaged"] is False
    assert audit["phi_included"] is False
