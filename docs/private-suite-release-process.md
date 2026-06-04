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
