from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PARTNER_INDEX = ROOT / "cases" / "partner" / "case_index.yaml"
GENERATED = ROOT / "partner-pack" / "generated"


def load_partner_cases() -> list[dict[str, Any]]:
    index = yaml.safe_load(PARTNER_INDEX.read_text(encoding="utf-8"))
    cases = index.get("cases", [])
    included: list[dict[str, Any]] = []
    for case in cases:
        path = Path(case["path"])
        if "private" in path.parts:
            raise SystemExit(f"private path in partner pack: {path}")
        case_dir = ROOT / path
        summary = json.loads((case_dir / "expected_receipt_summary.json").read_text())
        if summary.get("synthetic_data") is not True:
            raise SystemExit(f"case is not synthetic: {case['case_id']}")
        if not summary.get("expected_primary_error_code"):
            raise SystemExit(f"case lacks expected primary error: {case['case_id']}")
        if summary.get("private_case") is True:
            raise SystemExit(f"private-only case in partner pack: {case['case_id']}")
        included.append(
            {
                "case_id": case["case_id"],
                "path": str(path),
                "profile_version": case.get("profile_version", "v0.1.0"),
                "expected_primary_error_code": summary["expected_primary_error_code"],
                "synthetic_data": True,
                "no_phi": True,
            }
        )
    return included


def render_summary(cases: list[dict[str, Any]]) -> str:
    lines = [
        "# Partner Pack Summary",
        "",
        f"Included partner-safe cases: {len(cases)}",
        "",
        "Boundary: synthetic data only, no PHI, not clinical validation, not regulatory approval, not certification.",
        "",
        "| Case | Profile | Expected |",
        "| --- | --- | --- |",
    ]
    for case in cases:
        lines.append(
            f"| {case['case_id']} | {case['profile_version']} | "
            f"{case['expected_primary_error_code']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    cases = load_partner_cases()
    GENERATED.mkdir(parents=True, exist_ok=True)
    manifest = {
        "partner_pack_version": "v0.3.0",
        "included_case_count": len(cases),
        "private_cases_included": False,
        "no_phi": True,
        "boundary": [
            "not clinical validation",
            "not regulatory approval",
            "not certification",
            "synthetic partner-safe cases only",
        ],
        "cases": cases,
    }
    (GENERATED / "partner_pack_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (GENERATED / "partner_pack_summary.md").write_text(render_summary(cases), encoding="utf-8")
    print(json.dumps({"included_case_count": len(cases), "private_cases_included": False}, sort_keys=True))


if __name__ == "__main__":
    main()
