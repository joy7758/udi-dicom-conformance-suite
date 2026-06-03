from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_case_counts_and_required_fields() -> None:
    for section, minimum in [("partner", 15), ("private", 20)]:
        base = ROOT / "cases" / section
        cases = sorted(path for path in base.iterdir() if path.is_dir())
        assert len(cases) >= minimum
        for folder in cases:
            summary = json.loads((folder / "expected_receipt_summary.json").read_text())
            assert summary["expected_primary_error_code"]
            assert summary["synthetic_data"] is True


def test_case_index_yaml_after_generation() -> None:
    for section in ["partner", "private"]:
        index = yaml.safe_load((ROOT / "cases" / section / "case_index.yaml").read_text())
        assert "cases" in index
