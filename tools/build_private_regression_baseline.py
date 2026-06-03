from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "golden-outputs" / "private-regression-baseline.json"
DOC = ROOT / "docs" / "private-regression-baseline.md"


def iter_case_summaries() -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for section in ["partner", "private"]:
        for summary_path in sorted((ROOT / "cases" / section).rglob("expected_receipt_summary.json")):
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summaries.append(
                {
                    "section": section,
                    "profile_version": summary.get("profile_version", "v0.1.0"),
                    "expected_primary_error_code": summary["expected_primary_error_code"],
                    "synthetic_data": summary["synthetic_data"],
                }
            )
    return summaries


def build_baseline() -> dict[str, Any]:
    summaries = iter_case_summaries()
    by_error = Counter(item["expected_primary_error_code"] for item in summaries)
    by_profile = Counter(item["profile_version"] for item in summaries)
    by_section = Counter(item["section"] for item in summaries)
    return {
        "baseline_version": "v0.3.0",
        "internal_only": True,
        "case_count": len(summaries),
        "by_error_code": dict(sorted(by_error.items())),
        "by_profile_version": dict(sorted(by_profile.items())),
        "by_section": dict(sorted(by_section.items())),
        "planned_profile_versions": ["v0.1.0", "v0.2.0", "v0.3.0-planned"],
        "boundary": [
            "no PHI",
            "not clinical validation",
            "not regulatory approval",
            "not certification",
            "do not copy to public repo",
        ],
    }


def render_doc(baseline: dict[str, Any]) -> str:
    lines = [
        "# Private Regression Baseline",
        "",
        "Internal-only summary. Do not copy private baseline details to the public validator repository.",
        "",
        f"Total cases: {baseline['case_count']}",
        "",
        "## Profile Coverage",
        "",
    ]
    for profile, count in baseline["by_profile_version"].items():
        lines.append(f"- `{profile}`: {count}")
    lines.extend(["", "## Error Code Coverage", ""])
    for code, count in baseline["by_error_code"].items():
        lines.append(f"- `{code}`: {count}")
    lines.extend(
        [
            "",
            "Boundary: no PHI, not clinical validation, not regulatory approval, not certification.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    baseline = build_baseline()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DOC.write_text(render_doc(baseline), encoding="utf-8")
    print(
        json.dumps(
            {
                "case_count": baseline["case_count"],
                "profile_versions": baseline["by_profile_version"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
