from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_partner_pack_excludes_private_cases() -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_partner_pack.py")], check=True)
    manifest = json.loads(
        (ROOT / "partner-pack" / "generated" / "partner_pack_manifest.json").read_text()
    )
    assert manifest["included_case_count"] >= 25
    assert manifest["private_cases_included"] is False
    assert manifest["no_phi"] is True
    for case in manifest["cases"]:
        assert "cases/private" not in case["path"]
        assert case["synthetic_data"] is True
        assert case["no_phi"] is True
