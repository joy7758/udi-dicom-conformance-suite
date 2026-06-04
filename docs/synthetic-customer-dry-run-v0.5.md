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

