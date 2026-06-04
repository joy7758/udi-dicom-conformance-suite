from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "private-suite-release"
PARTNER_MANIFEST = ROOT / "partner-pack" / "generated" / "partner_pack_manifest.json"
PARTNER_SUMMARY = ROOT / "partner-pack" / "generated" / "partner_pack_summary.md"
BASELINE = ROOT / "golden-outputs" / "private-regression-baseline.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_case_index(section: str) -> list[dict[str, Any]]:
    path = ROOT / "cases" / section / "case_index.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")).get("cases", [])


def build_case_index_summary() -> dict[str, Any]:
    partner = load_case_index("partner")
    private = load_case_index("private")
    all_cases = partner + private
    return {
        "summary_version": "v0.4.0",
        "summary_only": True,
        "complete_private_case_manifest_included": False,
        "case_count": len(all_cases),
        "partner_case_count": len(partner),
        "private_case_count": len(private),
        "by_profile_version": dict(
            sorted(Counter(case.get("profile_version", "v0.1.0") for case in all_cases).items())
        ),
        "by_expected_primary_error_code": dict(
            sorted(Counter(case["expected_primary_error_code"] for case in all_cases).items())
        ),
        "boundary": [
            "private release only",
            "synthetic data only",
            "no PHI",
            "no raw DICOM",
            "not clinical validation",
            "not regulatory approval",
            "not certification",
        ],
    }


def copy_asset(source: Path, destination_name: str) -> Path:
    destination = OUT / destination_name
    shutil.copy2(source, destination)
    return destination


def build_assets() -> dict[str, Any]:
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_case_index.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_partner_pack.py")], check=True)
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_private_regression_baseline.py")],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "audit_partner_pack_leakage.py")],
        check=True,
    )
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    assets = [
        copy_asset(PARTNER_MANIFEST, "partner_pack_manifest.json"),
        copy_asset(PARTNER_SUMMARY, "partner_pack_summary.md"),
        copy_asset(BASELINE, "private_regression_baseline.json"),
    ]
    case_index_summary = build_case_index_summary()
    case_index_path = OUT / "case_index_summary.json"
    case_index_path.write_text(
        json.dumps(case_index_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    assets.append(case_index_path)
    checksums = {path.name: sha256(path) for path in assets}
    (OUT / "SHA256SUMS.txt").write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
        encoding="utf-8",
    )
    summary = {
        "asset_count": len(assets) + 1,
        "output_dir": str(OUT.relative_to(ROOT)),
        "private_release_only": True,
        "complete_private_case_manifest_included": False,
        "raw_dicom_included": False,
        "no_phi": True,
    }
    (OUT / "release_asset_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    print(json.dumps(build_assets(), sort_keys=True))


if __name__ == "__main__":
    main()
