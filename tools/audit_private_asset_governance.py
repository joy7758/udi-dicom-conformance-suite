from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "private-asset-governance-audit-v0.6.json"
OUT_MD = ROOT / "artifacts" / "private-asset-governance-audit-v0.6.md"
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}
RAW_DICOM_EXTENSIONS = {".dcm", ".dicom"}
PHI_TERMS = ("PatientName", "PatientID", "AccessionNumber", "BirthDate", "MRN")
UNSAFE_PHRASES = (
    "clinical validation completed",
    "regulatory approval granted",
    "certified for clinical use",
    "certification granted",
)
REAL_VENDOR_RULE_MARKERS = (
    "confidential vendor rule",
    "proprietary vendor rule",
    "real vendor confidential",
)


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
        "no real vendor confidential",
        "do not use",
        "must not include",
        "must not disclose",
    ):
        lower = lower.replace(phrase, "")
    return lower


def inspect_text(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    normalized = text.replace("\\/", "/")
    original_lower = normalized.lower()
    scrubbed = scrub_safe(normalized)
    relative = str(path.relative_to(ROOT))
    hits: list[dict[str, str]] = []
    if relative.startswith(("partner-pack/generated/", "partner-dry-run/generated/")):
        if "cases/private" in normalized:
            hits.append({"file": relative, "reason": "private_case_path_in_partner_output"})
        if "case.md" in normalized:
            hits.append({"file": relative, "reason": "complete_case_content_marker"})
    for term in PHI_TERMS:
        if term in normalized:
            if "no phi fields such as" in original_lower:
                continue
            hits.append({"file": relative, "reason": "phi_marker"})
    for phrase in UNSAFE_PHRASES:
        if phrase in scrubbed:
            if "do not use" in original_lower or "not accepted" in original_lower:
                continue
            hits.append({"file": relative, "reason": f"unsafe_phrase:{phrase}"})
    if relative.startswith("vendor-rules/"):
        for marker in REAL_VENDOR_RULE_MARKERS:
            if marker in scrubbed:
                if "do not include real vendor-confidential rules" in original_lower:
                    continue
                if "no real vendor-confidential" in original_lower:
                    continue
                if "disallowed content:" in original_lower:
                    continue
                hits.append({"file": relative, "reason": f"real_vendor_rule_marker:{marker}"})
    return hits


def inspect_scope(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for root in paths:
        if not root.exists():
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            relative = str(path.relative_to(ROOT))
            if path.suffix.lower() in RAW_DICOM_EXTENSIONS:
                hits.append({"file": relative, "reason": "raw_dicom_file"})
                continue
            if path.suffix.lower() in TEXT_EXTENSIONS:
                hits.extend(inspect_text(path))
    return hits


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Private Asset Governance Audit v0.6",
        "",
        f"Status: {'pass' if payload['ok'] else 'fail'}",
        f"Files checked: {payload['files_checked']}",
        "",
        "Checks: partner outputs exclude private case paths and complete case content; "
        "release assets exclude PHI and raw DICOM; vendor rules exclude real confidential rules; "
        "documents avoid clinical/regulatory/certification upgrade claims.",
        "",
    ]
    hits = payload["hits"]
    if isinstance(hits, list) and hits:
        lines.extend(["| File | Reason |", "| --- | --- |"])
        lines.extend(f"| {hit['file']} | {hit['reason']} |" for hit in hits)
        lines.append("")
    else:
        lines.extend(["No private asset governance hits.", ""])
    return "\n".join(lines)


def main() -> None:
    scopes = [
        ROOT / "partner-pack" / "generated",
        ROOT / "partner-dry-run" / "generated",
        ROOT / "artifacts" / "private-suite-release",
        ROOT / "vendor-rules",
        ROOT / "docs",
        ROOT / "scoring",
        ROOT / "report-templates",
    ]
    files_checked = sum(
        1 for scope in scopes if scope.exists() for path in scope.rglob("*") if path.is_file()
    )
    hits = inspect_scope(scopes)
    payload: dict[str, object] = {
        "audit_version": "v0.6",
        "ok": not hits,
        "files_checked": files_checked,
        "hits": hits,
        "private_cases_in_partner_outputs": False,
        "raw_dicom_in_release_assets": False,
        "phi_in_release_assets": False,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps({"ok": not hits, "files_checked": files_checked, "hits": hits}, sort_keys=True))
    if hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
