from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def case_folders(section: str) -> list[Path]:
    base = ROOT / "cases" / section
    return sorted(
        path
        for path in base.rglob("*")
        if path.is_dir() and (path / "expected_receipt_summary.json").exists()
    )


def test_case_counts_and_required_fields() -> None:
    for section, minimum in [("partner", 25), ("private", 35)]:
        cases = case_folders(section)
        assert len(cases) >= minimum
        for folder in cases:
            summary = json.loads((folder / "expected_receipt_summary.json").read_text())
            assert summary["expected_primary_error_code"]
            assert summary["synthetic_data"] is True


def test_case_index_yaml_after_generation() -> None:
    for section in ["partner", "private"]:
        index = yaml.safe_load((ROOT / "cases" / section / "case_index.yaml").read_text())
        assert "cases" in index
        assert any(case.get("profile_version") == "v0.2.0" for case in index["cases"])


def test_v02_case_counts() -> None:
    partner_v02 = [path for path in case_folders("partner") if "/v0_2/" in str(path)]
    private_v02 = [path for path in case_folders("private") if "/v0_2/" in str(path)]
    assert len(partner_v02) >= 10
    assert len(private_v02) >= 15
