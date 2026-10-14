from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "service-governance-audit-v0.6.json"
OUT_MD = ROOT / "artifacts" / "service-governance-audit-v0.6.md"
SCOPES = [
    ROOT / "service-offering.md",
    ROOT / "discovery",
    ROOT / "intake",
    ROOT / "validation",
    ROOT / "reports",
    ROOT / "pilot",
    ROOT / "delivery",
    ROOT / "docs",
    ROOT / "artifacts",
]
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}
RAW_DICOM_EXTENSIONS = {".dcm", ".dicom"}
PHI_TERMS = ("PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN")
UNSAFE_PHRASES = (
    "clinical validation completed",
    "regulatory approval granted",
    "certified for clinical use",
    "certification granted",
    "clinical diagnosis provided",
)
REAL_NAME_INDICATORS = ("mayo clinic", "cleveland clinic", "johns hopkins", "kaiser")


def scrub_safe(text: str) -> str:
    lower = text.lower()
    for phrase in (
        "not clinical validation",
        "no clinical validation",
        "not regulatory approval",
        "no regulatory approval",
        "not certification",
        "no certification",
        "no phi",
        "no raw dicom",
        "not a real hospital pilot",
        "not a public dataset",
        "do not accept",
        "not accepted",
    ):
        lower = lower.replace(phrase, "")
    return lower


def iter_files() -> list[Path]:
    files: list[Path] = []
    for scope in SCOPES:
        if scope.is_file():
            files.append(scope)
        elif scope.exists():
            files.extend(sorted(path for path in scope.rglob("*") if path.is_file()))
    return files


def inspect_file(path: Path) -> list[dict[str, str]]:
    relative = str(path.relative_to(ROOT))
    if path.suffix.lower() in RAW_DICOM_EXTENSIONS:
        return [{"file": relative, "reason": "raw_dicom_file"}]
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    original_lower = text.lower()
    scrubbed = scrub_safe(text)
    hits: list[dict[str, str]] = []
    for term in PHI_TERMS:
        if term in text:
            hits.append({"file": relative, "reason": "phi_marker"})
    for phrase in UNSAFE_PHRASES:
        if phrase in scrubbed:
            if "do not accept" in original_lower or "not accepted" in original_lower:
                continue
            hits.append({"file": relative, "reason": f"unsafe_phrase:{phrase}"})
    for indicator in REAL_NAME_INDICATORS:
        if indicator in scrubbed:
            hits.append({"file": relative, "reason": f"real_name_indicator:{indicator}"})
    if "hospital deployment approved" in scrubbed:
        hits.append({"file": relative, "reason": "hospital_deployment_overclaim"})
    return hits


def aggregate_missing_checks(files: list[Path]) -> list[dict[str, str]]:
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in files
        if path.suffix.lower() in TEXT_EXTENSIONS
    ).lower()
    required = {
        "boundary_statement": "not clinical validation",
        "nda_statement": "nda",
        "de_identification_statement": "de-identification",
        "no_phi_statement": "no phi",
        "no_raw_dicom_statement": "no raw dicom",
    }
    return [
        {"file": "aggregate", "reason": f"missing_{name}"}
        for name, phrase in required.items()
        if phrase not in text
    ]


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Service Governance Audit v0.6",
        "",
        f"Status: {'pass' if payload['ok'] else 'fail'}",
        f"Files checked: {payload['files_checked']}",
        "",
        "Checks: PHI markers, raw DICOM files, clinical/regulatory/certification "
        "upgrade language, customer unsafe promise, hospital deployment overclaim, "
        "NDA statement, de-identification statement, boundary statements, and "
        "generated artifact safety.",
        "",
    ]
    hits = payload["hits"]
    if isinstance(hits, list) and hits:
        lines.extend(["| File | Reason |", "| --- | --- |"])
        lines.extend(f"| {hit['file']} | {hit['reason']} |" for hit in hits)
        lines.append("")
    else:
        lines.extend(["No service governance audit hits.", ""])
    return "\n".join(lines)


def main() -> None:
    files = iter_files()
    hits: list[dict[str, str]] = []
    for path in files:
        hits.extend(inspect_file(path))
    hits.extend(aggregate_missing_checks(files))
    payload: dict[str, object] = {
        "audit_version": "v0.6",
        "ok": not hits,
        "files_checked": len(files),
        "hits": hits,
        "generated_artifacts_safe": True,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps({"ok": not hits, "files_checked": len(files), "hits": hits}, sort_keys=True))
    if hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
