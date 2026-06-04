# Synthetic Customer Dry Run v0.5

The synthetic customer dry run simulates discovery, intake, validation, report,
delivery, and pilot handoff using synthetic material only.

Run:

```bash
python scripts/run_synthetic_customer_dry_run.py
python scripts/check_synthetic_customer_dry_run.py artifacts/synthetic-customer-dry-run
```

Generated files:

- `artifacts/synthetic-customer-dry-run/summary.json`
- `artifacts/synthetic-customer-dry-run/summary.md`
- `artifacts/synthetic-customer-dry-run/customer_safe_report.md`
- `artifacts/synthetic-customer-dry-run/customer_handoff_checklist.md`

Boundary: no PHI, no raw DICOM, no real customer names, no real hospital names,
not clinical validation, not regulatory approval, and not certification.

## v0.6 Safe Handoff Extension

After the synthetic customer dry run, build and check the v0.6 safe handoff
package:

```bash
python scripts/build_safe_handoff_package.py
python scripts/check_safe_handoff_package.py artifacts/safe-handoff-package-v0.6
```

The safe handoff package reuses synthetic dry-run and delivery audit-trail
outputs only. It adds a manifest, summary, customer boundary statement, next
step decision tree, and SHA-256 checksums. It does not include PHI, raw DICOM,
real clinical reports, real customer names, real hospital names, clinical
validation, regulatory approval, or certification.
