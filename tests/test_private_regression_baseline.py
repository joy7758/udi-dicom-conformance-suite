from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_private_regression_baseline_is_summary_only() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_private_regression_baseline.py")],
        check=True,
    )
    baseline = json.loads(
        (ROOT / "golden-outputs" / "private-regression-baseline.json").read_text()
    )
    assert baseline["internal_only"] is True
    assert baseline["case_count"] >= 60
    assert baseline["by_section"]["partner"] >= 25
    assert baseline["by_section"]["private"] >= 35
    assert "v0.2.0" in baseline["by_profile_version"]
