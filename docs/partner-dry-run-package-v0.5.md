# Partner Dry Run Package v0.5

The partner dry run package is a partner-safe review surface generated from
`cases/partner/case_index.yaml`. It summarizes case identifiers, profile
versions, and expected primary error codes without copying full case content.

Build:

```bash
python tools/build_partner_dry_run_package.py
python tools/check_partner_dry_run_package.py partner-dry-run/generated
```

Generated files:

- `partner-dry-run/generated/partner_dry_run_manifest.json`
- `partner-dry-run/generated/partner_dry_run_summary.md`
- `partner-dry-run/generated/expected_partner_questions.md`
- `partner-dry-run/generated/partner_safe_case_table.md`

Boundary: partner-safe synthetic cases only, no PHI, no raw DICOM files, no
complete private case content, not clinical validation, not regulatory approval,
and not certification.

v0.6 adds partner feedback governance and private asset governance audit. Run
`tools/audit_private_asset_governance.py` before sharing partner-facing
summaries.
