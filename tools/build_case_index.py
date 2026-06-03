from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "manifest.json",
    "dicom_metadata.json",
    "registry_fixture.json",
    "expected_receipt_summary.json",
    "case.md",
}


def build(section: str) -> list[dict[str, object]]:
    base = ROOT / "cases" / section
    cases = []
    for folder in sorted(path for path in base.rglob("*") if path.is_dir()):
        if not (folder / "expected_receipt_summary.json").exists():
            continue
        missing = sorted(name for name in REQUIRED if not (folder / name).exists())
        if missing:
            raise SystemExit(f"{folder} missing {missing}")
        summary = json.loads((folder / "expected_receipt_summary.json").read_text())
        cases.append(
            {
                "case_id": folder.name,
                "path": str(folder.relative_to(ROOT)),
                "expected_primary_error_code": summary["expected_primary_error_code"],
                "profile_version": summary.get("profile_version", "v0.1.0"),
                "synthetic_data": summary["synthetic_data"],
            }
        )
    (base / "case_index.yaml").write_text(yaml.safe_dump({"cases": cases}, sort_keys=True))
    return cases


def main() -> None:
    total = build("partner") + build("private")
    print(f"indexed_cases={len(total)}")


if __name__ == "__main__":
    main()
