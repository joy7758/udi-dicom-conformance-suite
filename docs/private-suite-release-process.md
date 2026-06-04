# Private Suite Release Process

The private suite release package is internal/private only. It is intended for
partner pack review, private regression evidence, and synthetic conformance
workflow maintenance.

Build:

```bash
python tools/build_case_index.py
python tools/build_partner_pack.py
python tools/audit_partner_pack_leakage.py
python tools/build_private_regression_baseline.py
python tools/build_private_suite_release_assets.py
```

Generated assets are written to `artifacts/private-suite-release/`:

- `partner_pack_manifest.json`
- `partner_pack_summary.md`
- `private_regression_baseline.json`
- `case_index_summary.json`
- `release_asset_summary.json`
- `SHA256SUMS.txt`

The package does not include the complete private case manifest, raw DICOM
files, PHI, real patient data, real hospital data, or real vendor-confidential
rules.

This is not clinical validation, not regulatory approval, and not certification.

v0.5 pre-review adds:

```bash
python tools/build_partner_dry_run_package.py
python tools/check_partner_dry_run_package.py partner-dry-run/generated
python tools/audit_evidence_boundary.py
```

The dry run package is partner-safe and summary-only. The evidence boundary
audit is a release gate for no PHI, no raw DICOM files, no partner leakage of
private cases, no clinical validation, no regulatory approval, and no
certification upgrade language.

v0.6 pre-review adds:

```bash
python tools/audit_private_asset_governance.py
```

This audit verifies partner feedback governance, private asset handling, private
case lifecycle boundaries, and public paper support boundaries.
