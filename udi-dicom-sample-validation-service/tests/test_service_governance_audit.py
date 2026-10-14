from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_service_governance_audit_passes() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_synthetic_customer_dry_run.py")],
        check=True,
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_service_governance.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["hits"] == []

