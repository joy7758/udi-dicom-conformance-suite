from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PARTNER_INDEX = ROOT / "cases" / "partner" / "case_index.yaml"
OUT = ROOT / "partner-dry-run" / "generated"


def load_partner_safe_cases() -> list[dict[str, Any]]:
    index = yaml.safe_load(PARTNER_INDEX.read_text(encoding="utf-8"))
    cases: list[dict[str, Any]] = []
    for case in index.get("cases", []):
        path = Path(case["path"])
        if "private" in path.parts:
            raise SystemExit(f"private path blocked from partner dry run: {path}")
        summary_path = ROOT / path / "expected_receipt_summary.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("synthetic_data") is not True:
            raise SystemExit(f"non-synthetic partner case blocked: {case['case_id']}")
        if summary.get("private_case") is True:
            raise SystemExit(f"private case blocked: {case['case_id']}")
        cases.append(
            {
                "case_id": case["case_id"],
                "profile_version": case.get("profile_version", "v0.1.0"),
                "expected_primary_error_code": case["expected_primary_error_code"],
                "synthetic_data": True,
                "no_phi": True,
                "partner_safe": True,
            }
        )
    return cases


def render_summary(cases: list[dict[str, Any]]) -> str:
    by_profile = Counter(case["profile_version"] for case in cases)
    lines = [
        "# Partner Dry Run Summary v0.5",
        "",
        f"Partner-safe case count: {len(cases)}",
        "",
        "Profile coverage:",
    ]
    lines.extend(f"- {profile}: {count}" for profile, count in sorted(by_profile.items()))
    lines.extend(
        [
            "",
            "Boundary:",
            "",
            "- synthetic partner-safe cases only",
            "- no PHI",
            "- no raw DICOM files",
            "- no complete private case content",
            "- not clinical validation",
            "- not regulatory approval",
            "- not certification",
            "",
            "Dry run status: ready for technical partner review.",
            "",
        ]
    )
    return "\n".join(lines)


def render_questions() -> str:
    questions = [
        (
            "Why do you require de-identified or synthetic samples?",
            "To keep technical review separate from PHI handling and clinical operations.",
        ),
        (
            "Is the public validator a certification service?",
            "No. It is a deterministic evidence consistency checker for review outputs.",
        ),
        (
            "What is the difference between partner pack and private suite?",
            "The partner pack is summary-only and partner-safe; the private suite keeps internal cases.",
        ),
        (
            "Why use registry fixtures first?",
            "Offline fixtures keep review deterministic; live lookup must be explicitly enabled.",
        ),
        (
            "What does FDO-style mapping mean?",
            "It is optional metadata alignment, not an official FDO implementation claim.",
        ),
    ]
    lines = ["# Expected Partner Questions v0.5", "", "| Question | Safe Answer |", "| --- | --- |"]
    lines.extend(f"| {question} | {answer} |" for question, answer in questions)
    lines.append("")
    return "\n".join(lines)


def render_case_table(cases: list[dict[str, Any]]) -> str:
    lines = [
        "# Partner-Safe Case Table v0.5",
        "",
        "| Case | Profile | Expected Primary Error |",
        "| --- | --- | --- |",
    ]
    for case in cases:
        lines.append(
            "| {case_id} | {profile_version} | {expected_primary_error_code} |".format(**case)
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    cases = load_partner_safe_cases()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "package_version": "v0.5",
        "partner_safe_case_count": len(cases),
        "private_cases_included": False,
        "complete_private_case_content_included": False,
        "raw_dicom_included": False,
        "no_phi": True,
        "boundary": [
            "synthetic partner-safe cases only",
            "not clinical validation",
            "not regulatory approval",
            "not certification",
        ],
        "cases": cases,
    }
    (OUT / "partner_dry_run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "partner_dry_run_summary.md").write_text(render_summary(cases), encoding="utf-8")
    (OUT / "expected_partner_questions.md").write_text(render_questions(), encoding="utf-8")
    (OUT / "partner_safe_case_table.md").write_text(render_case_table(cases), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUT.relative_to(ROOT)),
                "partner_safe_case_count": len(cases),
                "private_cases_included": False,
                "raw_dicom_included": False,
                "no_phi": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
