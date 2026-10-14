from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_delivery_package_builder_and_checker() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_delivery_package.py"), "--synthetic-demo"],
        check=True,
    )
    generated = ROOT / "delivery" / "generated"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_delivery_package.py"), str(generated)],
        check=True,
    )
    manifest = json.loads((generated / "delivery_manifest_v0.3.json").read_text())
    assert manifest["raw_dicom_packaged"] is False
    assert manifest["forbidden_artifacts_packaged"] is False
