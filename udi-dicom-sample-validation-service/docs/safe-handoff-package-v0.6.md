# Safe Handoff Package v0.6

Build:

```bash
python scripts/build_safe_handoff_package.py
python scripts/check_safe_handoff_package.py artifacts/safe-handoff-package-v0.6
```

Outputs:

- `safe_handoff_manifest.json`
- `safe_handoff_summary.md`
- `customer_boundary_statement.md`
- `next_step_decision_tree.md`
- `SHA256SUMS.txt`

The package uses synthetic customer dry run and delivery audit trail summaries.
It contains no PHI, no raw DICOM, no real customer names, no real hospital
names, no clinical diagnosis, no regulatory approval, and no certification.

## v0.7 Prep Note

Before using safe handoff material in any customer review conversation, run the
v0.7 prep checklist in `docs/v0.7-safe-handoff-review-checklist.md`. This keeps
the package in technical-review scope and prevents clinical, regulatory, or
certification overclaiming.
