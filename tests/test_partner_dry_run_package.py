from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_partner_dry_run_package_build_and_check() -> None:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_partner_dry_run_package.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    build_payload = json.loads(build.stdout)
    assert build_payload["partner_safe_case_count"] >= 25
    assert build_payload["private_cases_included"] is False
    assert build_payload["raw_dicom_included"] is False

    check = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "check_partner_dry_run_package.py"),
            "partner-dry-run/generated",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    check_payload = json.loads(check.stdout)
    assert check_payload["ok"] is True
    assert check_payload["hits"] == []


def test_evidence_boundary_audit_passes() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_partner_dry_run_package.py")],
        check=True,
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "audit_evidence_boundary.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["hits"] == []
