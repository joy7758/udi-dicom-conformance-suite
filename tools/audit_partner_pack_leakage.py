from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "partner-pack" / "generated"
FORBIDDEN_PATH_MARKERS = ("cases/private", "private/")
FORBIDDEN_FIELDS = ("PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN")
FORBIDDEN_EXTENSIONS = (".dcm", ".dicom")
FORBIDDEN_UNBOUNDED_PHRASES = (
    "clinical diagnosis",
    "regulatory approval",
    "certification",
)
ALLOWED_BOUNDARY_PHRASES = (
    "not regulatory approval",
    "not certification",
    "not clinical validation",
)


def scrub_allowed_boundary_phrases(text: str) -> str:
    scrubbed = text
    for phrase in ALLOWED_BOUNDARY_PHRASES:
        scrubbed = scrubbed.replace(phrase, "")
    return scrubbed


def inspect_text(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    normalized = text.replace("\\/", "/")
    scrubbed = scrub_allowed_boundary_phrases(normalized)
    hits: list[dict[str, str]] = []
    for marker in FORBIDDEN_PATH_MARKERS:
        if marker in normalized:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": f"private_path:{marker}"})
    if "private-only" in normalized.lower() or '"private_case": true' in normalized.lower():
        hits.append({"file": str(path.relative_to(ROOT)), "reason": "private_only_marker"})
    for field in FORBIDDEN_FIELDS:
        if field in normalized:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": f"phi_field:{field}"})
    lower_scrubbed = scrubbed.lower()
    for phrase in FORBIDDEN_UNBOUNDED_PHRASES:
        if phrase in lower_scrubbed:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": f"unbounded_phrase:{phrase}"})
    return hits


def audit() -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    if not TARGET.exists():
        return {"ok": False, "hits": [{"file": str(TARGET), "reason": "missing_partner_pack"}]}
    for path in sorted(item for item in TARGET.rglob("*") if item.is_file()):
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            hits.append({"file": str(path.relative_to(ROOT)), "reason": "raw_dicom_file"})
            continue
        if path.suffix.lower() in {".json", ".md", ".txt", ".yaml", ".yml"}:
            hits.extend(inspect_text(path))
    return {
        "ok": not hits,
        "target": str(TARGET.relative_to(ROOT)),
        "hits": hits,
        "checks": [
            "no cases/private paths",
            "no private-only markers",
            "no raw DICOM files",
            "no PHI fields",
            "no unbounded certification or regulatory approval language",
        ],
    }


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
