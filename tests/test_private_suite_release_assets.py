from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "private-suite-release"


def test_private_suite_release_assets_are_summary_only() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_private_suite_release_assets.py")],
        check=True,
    )
    summary = json.loads((OUT / "release_asset_summary.json").read_text(encoding="utf-8"))
    case_index = json.loads((OUT / "case_index_summary.json").read_text(encoding="utf-8"))
    assert summary["private_release_only"] is True
    assert summary["complete_private_case_manifest_included"] is False
    assert summary["raw_dicom_included"] is False
    assert summary["no_phi"] is True
    assert case_index["summary_only"] is True
    assert case_index["complete_private_case_manifest_included"] is False
    assert (OUT / "SHA256SUMS.txt").exists()
