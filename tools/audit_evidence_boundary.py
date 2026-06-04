from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "artifacts" / "evidence-boundary-audit-v0.5.json"
OUTPUT_MD = ROOT / "artifacts" / "evidence-boundary-audit-v0.5.md"
SCOPES = (
    ROOT / "cases",
    ROOT / "partner-pack",
    ROOT / "partner-dry-run",
    ROOT / "scoring",
    ROOT / "report-templates",
    ROOT / "vendor-rules",
    ROOT / "docs",
)
TEXT_EXTENSIONS = {".json", ".md", ".txt", ".yaml", ".yml", ".csv"}
FORBIDDEN_EXTENSIONS = {".dcm", ".dicom"}
PHI_FIELDS = ("PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN")
UNSAFE_PHRASES = (
    "clinical diagnosis provided",
    "regulatory approval granted",
    "certified for clinical use",
    "certification granted",
    "hospital deployment approved",
    "real customer acceptance",
)
REAL_NAME_INDICATORS = (
    "mayo clinic",
    "cleveland clinic",
    "mass general",
    "johns hopkins",
    "kaiser permanente",
)


def scrub_safe_boundary(text: str) -> str:
    scrubbed = text.lower()
    safe_phrases = (
        "not clinical validation",
        "no clinical validation",
        "not regulatory approval",
        "no regulatory approval",
        "not certification",
        "no certification",
        "not a certification",
        "no phi",
        "no raw dicom",
        "no real hospital",
        "no real customer",
        "does not claim certification",
        "does not imply certification",
        "does not imply regulatory approval",
    )
    for phrase in safe_phrases:
        scrubbed = scrubbed.replace(phrase, "")
    return scrubbed


def inspect_file(path: Path) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    relative = str(path.relative_to(ROOT))
    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        return [{"file": relative, "reason": "raw_dicom_file"}]
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return hits
    text = path.read_text(encoding="utf-8")
    normalized = text.replace("\\/", "/")
    scrubbed = scrub_safe_boundary(normalized)
    lower_scrubbed = scrubbed.lower()
    if (
        relative.startswith(("partner-pack/generated/", "partner-dry-run/generated/"))
        and "cases/private" in normalized
    ):
        hits.append({"file": relative, "reason": "private_path_in_partner_output"})
    if "partner-dry-run/generated" in relative and "case.md" in normalized:
        hits.append({"file": relative, "reason": "complete_case_content_in_partner_output"})
    for field in PHI_FIELDS:
        if field in normalized and "no PHI fields such as" not in normalized:
            hits.append({"file": relative, "reason": f"phi_field:{field}"})
    for phrase in UNSAFE_PHRASES:
        if phrase in lower_scrubbed:
            if "do not use" in lower_scrubbed or "checks include" in lower_scrubbed:
                continue
            hits.append({"file": relative, "reason": f"unsafe_phrase:{phrase}"})
    for indicator in REAL_NAME_INDICATORS:
        if indicator in lower_scrubbed:
            hits.append({"file": relative, "reason": f"real_name_indicator:{indicator}"})
    if "device uid is udi-di" in lower_scrubbed or "device uid equals udi-di" in lower_scrubbed:
        hits.append({"file": relative, "reason": "device_uid_confused_with_udi_di"})
    return hits


def iter_scope_files() -> list[Path]:
    files: list[Path] = []
    for scope in SCOPES:
        if not scope.exists():
            continue
        files.extend(sorted(path for path in scope.rglob("*") if path.is_file()))
    return files


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Evidence Boundary Audit v0.5",
        "",
        f"Status: {'pass' if payload['ok'] else 'fail'}",
        f"Files checked: {payload['files_checked']}",
        "",
        "Checks:",
        "",
        "- no raw DICOM files",
        "- no PHI fields outside explicit boundary examples",
        "- no private case paths in partner outputs",
        "- no clinical diagnosis, regulatory approval, or certification upgrade claims",
        "- no real customer or real hospital name indicators",
        "- Device UID is not treated as UDI-DI",
        "",
    ]
    hits = payload["hits"]
    if isinstance(hits, list) and hits:
        lines.extend(["| File | Reason |", "| --- | --- |"])
        lines.extend(f"| {hit['file']} | {hit['reason']} |" for hit in hits)
        lines.append("")
    else:
        lines.extend(["No boundary audit hits.", ""])
    return "\n".join(lines)


def main() -> None:
    files = iter_scope_files()
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
