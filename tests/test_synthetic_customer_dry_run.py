from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_customer_dry_run_outputs_are_safe() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_synthetic_customer_dry_run.py")],
        check=True,
    )
    out = ROOT / "artifacts" / "synthetic-customer-dry-run"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_synthetic_customer_dry_run.py"), str(out)],
        check=True,
    )
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "pass"
    assert summary["phi_included"] is False
    assert summary["raw_dicom_included"] is False
    assert summary["real_customer_included"] is False
    assert summary["real_hospital_included"] is False


def test_service_language_audit_passes() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_synthetic_customer_dry_run.py")],
        check=True,
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_service_language.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["hits"] == []
    assert (ROOT / "artifacts" / "service-language-audit-v0.5.json").exists()
    assert (ROOT / "artifacts" / "service-language-audit-v0.5.md").exists()
