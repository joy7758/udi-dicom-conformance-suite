from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_evidence_boundary_audit_outputs_artifacts() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_partner_dry_run_package.py")],
        check=True,
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "audit_evidence_boundary.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert (ROOT / "artifacts" / "evidence-boundary-audit-v0.5.json").exists()
    assert (ROOT / "artifacts" / "evidence-boundary-audit-v0.5.md").exists()
