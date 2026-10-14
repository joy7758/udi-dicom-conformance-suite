from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "safe-handoff-package-v0.6"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)


def render_summary(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Safe Handoff Summary v0.6",
            "",
            f"Package id: `{manifest['package_id']}`",
            f"Synthetic customer dry run: `{manifest['synthetic_customer_dry_run']}`",
            f"Delivery audit trail: `{manifest['delivery_audit_trail']}`",
            "",
            "Boundary: technical review only; no PHI; no raw DICOM; no real customer names; "
            "no real hospital names; not clinical validation; not regulatory approval; "
            "not certification.",
            "",
        ]
    )


def render_boundary_statement() -> str:
    return "\n".join(
        [
            "# Customer Boundary Statement",
            "",
            "This safe handoff package is synthetic technical review material only.",
            "It contains no PHI, no raw DICOM, no real clinical report, no real customer "
            "names, and no real hospital names.",
            "",
            "It is not clinical validation, not regulatory approval, not certification, "
            "not a clinical diagnosis, and not hospital deployment approval.",
            "",
            "Any real cooperation requires NDA and de-identification gates.",
            "",
        ]
    )


def render_decision_tree() -> str:
    return "\n".join(
        [
            "# Next Step Decision Tree",
            "",
            "1. If feedback is about synthetic documentation, triage as documentation.",
            "2. If feedback concerns delivery package content, run delivery and handoff checks.",
            "3. If PHI or raw DICOM is requested, stop and escalate.",
            "4. If clinical validation, regulatory approval, or certification is requested, mark out of scope.",
            "5. If real cooperation is requested, require NDA and de-identification review first.",
            "",
        ]
    )


def main() -> None:
    run([sys.executable, "scripts/run_synthetic_customer_dry_run.py"])
    run([sys.executable, "scripts/build_delivery_audit_trail.py", "--synthetic-demo"])
    summary_path = ROOT / "artifacts" / "synthetic-customer-dry-run" / "summary.json"
    audit_path = ROOT / "delivery" / "generated" / "delivery_audit_trail_v0.4.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "package_id": "safe-handoff-v0.6-001",
        "package_version": "v0.6",
        "synthetic_customer_dry_run": str(summary_path.relative_to(ROOT)),
        "delivery_audit_trail": str(audit_path.relative_to(ROOT)),
        "redaction_check_status": summary.get("redaction_check_status"),
        "delivery_audit_status": audit.get("forbidden_asset_check_status"),
        "phi_included": False,
        "raw_dicom_included": False,
        "real_customer_included": False,
        "real_hospital_included": False,
        "boundary_statement_included": True,
        "boundary": [
            "technical review only",
            "no PHI",
            "no raw DICOM",
            "not clinical validation",
            "not regulatory approval",
            "not certification",
            "NDA and de-identification required for real cooperation",
        ],
    }
    (OUT / "safe_handoff_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "safe_handoff_summary.md").write_text(render_summary(manifest), encoding="utf-8")
    (OUT / "customer_boundary_statement.md").write_text(
        render_boundary_statement(),
        encoding="utf-8",
    )
    (OUT / "next_step_decision_tree.md").write_text(render_decision_tree(), encoding="utf-8")
    files = sorted(path for path in OUT.iterdir() if path.is_file() and path.name != "SHA256SUMS.txt")
    (OUT / "SHA256SUMS.txt").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in files),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"ok": True, "output": str(OUT.relative_to(ROOT)), "raw_dicom_included": False},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
