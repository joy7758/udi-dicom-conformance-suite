from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_safe_handoff_package_build_and_check() -> None:
    build = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_safe_handoff_package.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(build.stdout)
    assert payload["ok"] is True
    check = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_safe_handoff_package.py"),
            "artifacts/safe-handoff-package-v0.6",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    checked = json.loads(check.stdout)
    assert checked["ok"] is True
