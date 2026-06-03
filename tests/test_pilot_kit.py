from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pilot_kit_generated_without_deployment_or_price_promises() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_pilot_kit.py")], check=True)
    generated = ROOT / "pilot" / "generated"
    required = [
        "pilot_readiness_checklist.md",
        "pilot_scope_template.md",
        "pilot_success_criteria.md",
        "pilot_boundary_statement.md",
    ]
    for name in required:
        text = (generated / name).read_text()
        assert "$" not in text
        assert "hospital-level deployment promise" in text or "not hospital-level deployment" in text
    boundary = (generated / "pilot_boundary_statement.md").read_text()
    assert "not clinical validation" in boundary
    assert "not regulatory approval" in boundary
    assert "not certification" in boundary
