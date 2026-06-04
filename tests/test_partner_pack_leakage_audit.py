from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_partner_pack_leakage_audit_passes_generated_pack() -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_partner_pack.py")], check=True)
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "audit_partner_pack_leakage.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["hits"] == []
