from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FILES = {
    "summary.json",
    "summary.md",
    "customer_safe_report.md",
    "customer_handoff_checklist.md",
}
FORBIDDEN_EXTENSIONS = {".dcm", ".dicom"}
FORBIDDEN_TERMS = {"PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN"}
UNSAFE_PHRASES = {
    "clinical diagnosis provided",
    "regulatory approval granted",
    "certified for clinical use",
    "compliance certificate issued",
    "hospital deployment approved",
}


def inspect_text(path: Path) -> list[str]:
    hits: list[str] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    for term in FORBIDDEN_TERMS:
        if term in text:
            hits.append(f"phi_marker:{term}:{path}")
    for phrase in UNSAFE_PHRASES:
        if phrase in lower:
            hits.append(f"unsafe_phrase:{phrase}:{path}")
    return hits


def check(path: Path) -> dict[str, object]:
    hits: list[str] = []
    for name in sorted(REQUIRED_FILES):
        if not (path / name).exists():
            hits.append(f"missing:{name}")
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        if item.suffix.lower() in FORBIDDEN_EXTENSIONS:
            hits.append(f"raw_dicom:{item}")
            continue
        if item.suffix.lower() in {".json", ".md", ".txt", ".yaml", ".yml"}:
            hits.extend(inspect_text(item))
    if not hits:
        summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
        if summary.get("status") != "pass":
            hits.append("status_not_pass")
        if summary.get("phi_included") is not False:
            hits.append("phi_included_not_false")
        if summary.get("raw_dicom_included") is not False:
            hits.append("raw_dicom_included_not_false")
        if summary.get("real_customer_included") is not False:
            hits.append("real_customer_included_not_false")
        if summary.get("real_hospital_included") is not False:
            hits.append("real_hospital_included_not_false")
    return {"ok": not hits, "hits": hits}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    result = check(Path(args.path))
    print(json.dumps(result, sort_keys=True))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
