from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "synthetic-pilot-e2e"


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


def synthetic_receipt_summary() -> dict[str, Any]:
    return {
        "validator_version": "public-v0.3",
        "profile_version": "v0.2.0",
        "receipt_count": 1,
        "primary_error_code": None,
        "ok": True,
        "synthetic": True,
        "no_phi": True,
    }


def synthetic_partner_pack_summary() -> dict[str, Any]:
    return {
        "suite_version": "private-suite-v0.3",
        "partner_safe_case_count": 25,
        "private_cases_included": False,
        "synthetic": True,
        "no_phi": True,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Synthetic Pilot E2E Summary",
            "",
            f"Pilot id: `{summary['pilot_id']}`",
            f"Delivery generated: `{summary['delivery_package_generated']}`",
            f"Pilot kit generated: `{summary['pilot_kit_generated']}`",
            f"Redaction check: `{summary['redaction_check_status']}`",
            f"Delivery package check: `{summary['delivery_package_check_status']}`",
            "",
            "Boundary: synthetic-only, no PHI, no raw DICOM, not clinical validation, "
            "not regulatory approval, not certification.",
            "",
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    steps = [
        run([sys.executable, "scripts/build_service_readiness_matrix.py"]),
        run([sys.executable, "scripts/build_pilot_kit.py"]),
        run([sys.executable, "scripts/build_delivery_package.py", "--synthetic-demo"]),
        run([sys.executable, "scripts/redact_check.py", "."]),
        run([sys.executable, "scripts/check_delivery_package.py", "delivery/generated"]),
    ]
    failed = [step for step in steps if step["returncode"] != 0]
    summary = {
        "pilot_id": "synthetic-pilot-v0.4-001",
        "service_version": "v0.4.0-branch",
        "validator_receipt_summary": synthetic_receipt_summary(),
        "partner_pack_summary": synthetic_partner_pack_summary(),
        "batch_summary": "delivery/generated/synthetic_batch_summary_v0.3.json",
        "delivery_package_generated": not failed,
        "pilot_kit_generated": not failed,
        "redaction_check_status": "pass" if steps[3]["returncode"] == 0 else "fail",
        "delivery_package_check_status": "pass" if steps[4]["returncode"] == 0 else "fail",
        "raw_dicom_copied": False,
        "phi_included": False,
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
    (OUT / "summary.md").write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps({"ok": not failed, "output_dir": str(OUT.relative_to(ROOT))}, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
