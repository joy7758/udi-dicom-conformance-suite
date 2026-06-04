from __future__ import annotations

import argparse
import json
from pathlib import Path

FORBIDDEN_EXTENSIONS = {".dcm", ".dicom"}
FORBIDDEN_TERMS = {"PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN"}


def check(path: Path) -> dict[str, object]:
    hits: list[str] = []
    if not (path / "summary.json").exists():
        hits.append("missing_summary_json")
    if not (path / "summary.md").exists():
        hits.append("missing_summary_md")
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        if item.suffix.lower() in FORBIDDEN_EXTENSIONS:
            hits.append(f"raw_dicom:{item}")
        text = item.read_text(encoding="utf-8", errors="ignore")
        for term in FORBIDDEN_TERMS:
            if term in text:
                hits.append(f"phi_marker:{term}:{item}")
    if not hits:
        summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
        if summary.get("raw_dicom_copied") is not False:
            hits.append("raw_dicom_copied_not_false")
        if summary.get("phi_included") is not False:
            hits.append("phi_included_not_false")
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
