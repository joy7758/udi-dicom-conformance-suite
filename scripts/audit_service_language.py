from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "artifacts" / "service-language-audit-v0.5.json"
OUTPUT_MD = ROOT / "artifacts" / "service-language-audit-v0.5.md"
SCOPES = [
    ROOT / "service-offering.md",
    ROOT / "discovery",
    ROOT / "intake",
    ROOT / "validation",
    ROOT / "reports",
    ROOT / "pilot",
    ROOT / "delivery",
    ROOT / "docs",
    ROOT / "artifacts" / "synthetic-customer-dry-run",
]
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}
FORBIDDEN_EXTENSIONS = {".dcm", ".dicom"}
PHI_TERMS = ("PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN")
UNSAFE_PHRASES = (
    "clinical diagnosis provided",
    "clinical validation completed",
    "regulatory approval granted",
    "certified for clinical use",
    "compliance certificate issued",
    "hospital deployment approved",
)
REAL_NAME_INDICATORS = (
    "mayo clinic",
    "cleveland clinic",
    "mass general",
    "johns hopkins",
    "kaiser permanente",
)
PRICE_PATTERN = re.compile(r"\$\s?\d|usd\s?\d", re.IGNORECASE)


def scrub_safe_language(text: str) -> str:
    scrubbed = text.lower()
    safe_phrases = (
        "not clinical validation",
        "no clinical validation",
        "not regulatory approval",
        "no regulatory approval",
        "not certification",
        "no certification",
        "does not include phi",
        "no phi",
        "no raw dicom",
        "not hospital-level deployment",
        "no hospital-level deployment promise",
        "do not include price amounts or hospital-level deployment promises",
        "does not include phi, raw dicom",
    )
    for phrase in safe_phrases:
        scrubbed = scrubbed.replace(phrase, "")
    return scrubbed


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
    hits: list[dict[str, str]] = []
    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        return [{"file": relative, "reason": "raw_dicom_file"}]
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return hits
    text = path.read_text(encoding="utf-8", errors="ignore")
    scrubbed = scrub_safe_language(text)
    lower = scrubbed.lower()
    for term in PHI_TERMS:
        if term in text:
            hits.append({"file": relative, "reason": "phi_marker"})
    for phrase in UNSAFE_PHRASES:
        if phrase in lower:
            if "do not use" in lower or "must not" in lower:
                continue
            hits.append({"file": relative, "reason": f"unsafe_phrase:{phrase}"})
    for indicator in REAL_NAME_INDICATORS:
        if indicator in lower:
            hits.append({"file": relative, "reason": f"real_name_indicator:{indicator}"})
    if PRICE_PATTERN.search(text):
        hits.append({"file": relative, "reason": "pricing_overcommitment"})
    if (
        "hospital-level deployment promise" in lower
        and "no hospital-level deployment promise" not in text.lower()
        and "do not include price amounts or hospital-level deployment promises" not in text.lower()
    ):
        hits.append({"file": relative, "reason": "hospital_deployment_overclaim"})
    return hits


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Service Language Audit v0.5",
        "",
        f"Status: {'pass' if payload['ok'] else 'fail'}",
        f"Files checked: {payload['files_checked']}",
        "",
        "Checks cover PHI markers, raw DICOM inclusion risk, unsafe clinical, "
        "regulatory, certification, customer, hospital, and pricing language.",
        "",
    ]
    hits = payload["hits"]
    if isinstance(hits, list) and hits:
        lines.extend(["| File | Reason |", "| --- | --- |"])
        lines.extend(f"| {hit['file']} | {hit['reason']} |" for hit in hits)
        lines.append("")
    else:
        lines.extend(["No service language audit hits.", ""])
    return "\n".join(lines)


def main() -> None:
    files = iter_files()
    hits: list[dict[str, str]] = []
    for path in files:
        hits.extend(inspect_file(path))
    payload: dict[str, object] = {
        "audit_version": "v0.5",
        "ok": not hits,
        "files_checked": len(files),
        "hits": hits,
        "scopes": [str(scope.relative_to(ROOT)) for scope in SCOPES],
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps({"ok": not hits, "files_checked": len(files), "hits": hits}, sort_keys=True))
    if hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
