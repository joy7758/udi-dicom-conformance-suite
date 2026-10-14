from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    "safe_handoff_manifest.json",
    "safe_handoff_summary.md",
    "customer_boundary_statement.md",
    "next_step_decision_tree.md",
    "SHA256SUMS.txt",
}
RAW_DICOM_EXTENSIONS = {".dcm", ".dicom"}
PHI_TERMS = {"PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN"}
UNSAFE_PHRASES = {
    "clinical diagnosis provided",
    "regulatory approval granted",
    "certified for clinical use",
    "certification granted",
}
REAL_NAME_INDICATORS = {"mayo clinic", "cleveland clinic", "johns hopkins", "kaiser"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scrub_safe(text: str) -> str:
    lower = text.lower()
    for phrase in (
        "not clinical validation",
        "not regulatory approval",
        "not certification",
        "no phi",
        "no raw dicom",
        "not a clinical diagnosis",
    ):
        lower = lower.replace(phrase, "")
    return lower


def inspect_file(path: Path) -> list[str]:
    if path.suffix.lower() in RAW_DICOM_EXTENSIONS:
        return [f"raw_dicom:{path.name}"]
    text = path.read_text(encoding="utf-8", errors="ignore")
    scrubbed = scrub_safe(text)
    hits: list[str] = []
    for term in PHI_TERMS:
        if term in text:
            hits.append(f"phi_marker:{term}:{path.name}")
    for phrase in UNSAFE_PHRASES:
        if phrase in scrubbed:
            hits.append(f"unsafe_phrase:{phrase}:{path.name}")
    for indicator in REAL_NAME_INDICATORS:
        if indicator in scrubbed:
            hits.append(f"real_name_indicator:{indicator}:{path.name}")
    return hits


def check_checksums(path: Path) -> list[str]:
    failures: list[str] = []
    for line in (path / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        target = path / name
        if not target.exists():
            failures.append(f"missing_checksum_target:{name}")
        elif sha256(target) != digest:
            failures.append(f"checksum_mismatch:{name}")
    return failures


def main() -> None:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "artifacts" / "safe-handoff-package-v0.6"
    if not package.is_absolute():
        package = ROOT / package
    failures: list[str] = []
    for name in sorted(REQUIRED_FILES):
        if not (package / name).exists():
            failures.append(f"missing:{name}")
    if not failures:
        manifest = json.loads((package / "safe_handoff_manifest.json").read_text(encoding="utf-8"))
        if manifest.get("phi_included") is not False:
            failures.append("phi_included_not_false")
        if manifest.get("raw_dicom_included") is not False:
            failures.append("raw_dicom_included_not_false")
        if manifest.get("boundary_statement_included") is not True:
            failures.append("boundary_statement_missing")
        failures.extend(check_checksums(package))
    for path in sorted(item for item in package.rglob("*") if item.is_file()):
        if path.suffix.lower() in {".json", ".md", ".txt", ".yaml", ".yml"}:
            failures.extend(inspect_file(path))
        elif path.suffix.lower() in RAW_DICOM_EXTENSIONS:
            failures.append(f"raw_dicom:{path.name}")
    result = {"ok": not failures, "failures": failures, "package": str(package.relative_to(ROOT))}
    print(json.dumps(result, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
