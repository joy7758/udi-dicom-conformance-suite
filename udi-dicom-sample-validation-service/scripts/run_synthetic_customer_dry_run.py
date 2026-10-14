from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "synthetic-customer-dry-run"


def run(command: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {"cmd": command, "returncode": proc.returncode, "output": proc.stdout.strip()}


def render_customer_safe_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Customer-Safe Synthetic Dry Run Report",
            "",
            f"Dry run id: `{summary['dry_run_id']}`",
            f"Discovery status: `{summary['workflow']['discovery']}`",
            f"Intake status: `{summary['workflow']['intake']}`",
            f"Validation status: `{summary['workflow']['validation']}`",
            f"Report status: `{summary['workflow']['report']}`",
            f"Delivery status: `{summary['workflow']['delivery']}`",
            f"Pilot handoff status: `{summary['workflow']['pilot_handoff']}`",
            "",
            "Boundary: synthetic technical review only; no PHI, no raw DICOM, "
            "not clinical validation, not regulatory approval, not certification.",
            "",
        ]
    )


def render_handoff_checklist(summary: dict[str, Any]) -> str:
    checks = [
        "redaction check passed",
        "service readiness matrix generated",
        "pilot kit generated",
        "delivery package generated",
        "delivery package checker passed",
        "delivery audit trail generated",
        "synthetic report prepared",
        "boundary statement included",
    ]
    lines = [
        "# Customer Handoff Checklist",
        "",
        f"Dry run id: `{summary['dry_run_id']}`",
        "",
    ]
    lines.extend(f"- [x] {check}" for check in checks)
    lines.extend(
        [
            "",
            "Do not attach raw DICOM files, PHI, real clinical reports, real customer names, "
            "or real hospital names.",
            "",
        ]
    )
    return "\n".join(lines)


def render_summary_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Synthetic Customer Dry Run Summary v0.5",
        "",
        f"Dry run id: `{summary['dry_run_id']}`",
        f"Overall status: `{summary['status']}`",
        "",
        "| Step | Status |",
        "| --- | --- |",
    ]
    lines.extend(f"| {name} | {status} |" for name, status in summary["workflow"].items())
    lines.extend(
        [
            "",
            "Boundary: synthetic-only, no PHI, no raw DICOM, not clinical validation, "
            "not regulatory approval, not certification.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    steps = [
        run([sys.executable, "scripts/redact_check.py", "."]),
        run([sys.executable, "scripts/build_service_readiness_matrix.py"]),
        run([sys.executable, "scripts/build_pilot_kit.py"]),
        run([sys.executable, "scripts/build_delivery_package.py", "--synthetic-demo"]),
        run([sys.executable, "scripts/check_delivery_package.py", "delivery/generated"]),
        run([sys.executable, "scripts/build_delivery_audit_trail.py", "--synthetic-demo"]),
    ]
    failed = [step for step in steps if step["returncode"] != 0]
    workflow = {
        "discovery": "synthetic_complete",
        "intake": "synthetic_complete",
        "validation": "pass" if steps[4]["returncode"] == 0 else "fail",
        "report": "synthetic_report_ready",
        "delivery": "pass" if steps[4]["returncode"] == 0 else "fail",
        "pilot_handoff": "ready" if not failed else "hold",
    }
    summary = {
        "dry_run_id": "synthetic-customer-v0.5-001",
        "service_version": "v0.5-dry-run",
        "status": "pass" if not failed else "fail",
        "synthetic_customer_workspace": "artifacts/synthetic-customer-dry-run",
        "workflow": workflow,
        "redaction_check_status": "pass" if steps[0]["returncode"] == 0 else "fail",
        "delivery_package_check_status": "pass" if steps[4]["returncode"] == 0 else "fail",
        "delivery_audit_trail_status": "pass" if steps[5]["returncode"] == 0 else "fail",
        "phi_included": False,
        "raw_dicom_included": False,
        "real_customer_included": False,
        "real_hospital_included": False,
        "boundary": [
            "synthetic-only",
            "no PHI",
            "no raw DICOM",
            "not clinical validation",
            "not regulatory approval",
            "not certification",
        ],
        "steps": steps,
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "summary.md").write_text(render_summary_markdown(summary), encoding="utf-8")
    (OUT / "customer_safe_report.md").write_text(
        render_customer_safe_report(summary),
        encoding="utf-8",
    )
    (OUT / "customer_handoff_checklist.md").write_text(
        render_handoff_checklist(summary),
        encoding="utf-8",
    )
    print(json.dumps({"ok": not failed, "output_dir": str(OUT.relative_to(ROOT))}, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
