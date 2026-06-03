from __future__ import annotations

import argparse
import json
from pathlib import Path

FORBIDDEN_EXTENSIONS = {".dcm"}
FORBIDDEN_PHRASES = {
    "PatientName",
    "PatientID",
    "AccessionNumber",
    "BirthDate",
    "MRN",
    "clinical diagnosis",
    "certification",
}
ALLOWED_BOUNDARY_PHRASES = {
    "not certification",
    "not clinical validation",
    "not regulatory approval",
}


def check(root: Path) -> dict[str, object]:
    hits: list[str] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.suffix in FORBIDDEN_EXTENSIONS:
            hits.append(f"forbidden_extension:{path}")
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                if phrase == "certification" and any(boundary in text for boundary in ALLOWED_BOUNDARY_PHRASES):
                    continue
                hits.append(f"forbidden_phrase:{phrase}:{path}")
    manifest_path = root / "delivery_manifest_v0.3.json"
    if not manifest_path.exists():
        hits.append("missing_delivery_manifest_v0.3.json")
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("raw_dicom_packaged") is not False:
            hits.append("raw_dicom_packaged_not_false")
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
