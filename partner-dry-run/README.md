# Partner Dry Run v0.5

This directory holds generated partner-safe dry run material. It is intended for
technical review discussion before any real sample or NDA-controlled workflow.

Generate:

```bash
python tools/build_partner_dry_run_package.py
python tools/check_partner_dry_run_package.py partner-dry-run/generated
```

Boundary: synthetic partner-safe cases only, no PHI, no raw DICOM files, no
complete private case content, not clinical validation, not regulatory approval,
and not certification.

