from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_private_asset_governance_audit_passes() -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_partner_pack.py")], check=True)
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_partner_dry_run_package.py")],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_private_suite_release_assets.py")],
        check=True,
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "audit_private_asset_governance.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["hits"] == []
    assert (ROOT / "artifacts" / "private-asset-governance-audit-v0.6.json").exists()
    assert (ROOT / "artifacts" / "private-asset-governance-audit-v0.6.md").exists()
