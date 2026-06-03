from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_templates_exist_and_contain_boundaries() -> None:
    required = [
        ROOT / "reports/templates/sample-validation-report.md",
        ROOT / "reports/templates/executive-summary.md",
        ROOT / "service-offering.md",
    ]
    for path in required:
        text = path.read_text(encoding="utf-8")
        assert "not clinical validation" in text
        assert "not regulatory approval" in text
        assert "no PHI" in text
        assert "not certification" in text
