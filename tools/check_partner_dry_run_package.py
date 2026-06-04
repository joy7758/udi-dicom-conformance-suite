from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    "partner_dry_run_manifest.json",
    "partner_dry_run_summary.md",
    "expected_partner_questions.md",
    "partner_safe_case_table.md",
}
FORBIDDEN_PATH_MARKERS = ("cases/private", "private/")
FORBIDDEN_FIELDS = ("PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN")
FORBIDDEN_EXTENSIONS = (".dcm", ".dicom")
FORBIDDEN_UNSAFE_PHRASES = (
    "clinical diagnosis",
    "regulatory approval granted",
    "certified for clinical use",
    "certification granted",
    "hospital deployment approved",
)


def scrub_boundary_phrases(text: str) -> str:
    scrubbed = text.lower()
    allowed = (
        "not clinical validation",
        "not regulatory approval",
        "not certification",
        "no certification",
        "no phi",
        "no raw dicom",
        "is not a certification service",
    )
    for phrase in allowed:
        scrubbed = scrubbed.replace(phrase, "")
    return scrubbed


def inspect_text(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    normalized = text.replace("\\/", "/")
    scrubbed = scrub_boundary_phrases(normalized)
    hits: list[dict[str, str]] = []
    for marker in FORBIDDEN_PATH_MARKERS:
        if marker in normalized:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": f"private_path:{marker}"})
    for field in FORBIDDEN_FIELDS:
        if field in normalized:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": f"phi_field:{field}"})
    for phrase in FORBIDDEN_UNSAFE_PHRASES:
        if phrase in scrubbed:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": f"unsafe_phrase:{phrase}"})
    return hits


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "partner-dry-run" / "generated"
    if not target.is_absolute():
        target = ROOT / target
    hits: list[dict[str, str]] = []
    for name in sorted(REQUIRED_FILES):
        if not (target / name).exists():
            hits.append({"file": str((target / name).relative_to(ROOT)), "reason": "missing"})
    if not hits:
        manifest = load_manifest(target / "partner_dry_run_manifest.json")
        if manifest.get("partner_safe_case_count", 0) < 25:
            hits.append({"file": str(target.relative_to(ROOT)), "reason": "too_few_partner_cases"})
        if manifest.get("private_cases_included") is not False:
            hits.append({"file": str(target.relative_to(ROOT)), "reason": "private_cases_included"})
        if manifest.get("raw_dicom_included") is not False:
            hits.append({"file": str(target.relative_to(ROOT)), "reason": "raw_dicom_included"})
        if manifest.get("no_phi") is not True:
            hits.append({"file": str(target.relative_to(ROOT)), "reason": "no_phi_not_true"})
    for path in sorted(item for item in target.rglob("*") if item.is_file()):
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": "raw_dicom_file"})
            continue
        if path.suffix.lower() in {".json", ".md", ".txt", ".yaml", ".yml"}:
            hits.extend(inspect_text(path))
    result = {"ok": not hits, "target": str(target.relative_to(ROOT)), "hits": hits}
    print(json.dumps(result, indent=2, sort_keys=True))
    if hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
