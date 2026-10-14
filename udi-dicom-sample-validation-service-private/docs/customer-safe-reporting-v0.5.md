# Customer-Safe Reporting v0.5

Customer-safe reports use:

- `reports/templates/customer-safe-summary.md`
- `reports/templates/customer-safe-finding-table.md`
- `reports/templates/customer-safe-remediation-plan.md`
- `reports/templates/customer-safe-boundary-statement.md`

Reports must stay technical. They may summarize receipt status, evidence
consistency findings, redaction check status, and delivery readiness. They must
not provide diagnosis, regulatory clearance, certification, compliance
certificate language, or hospital deployment promises.

## v0.6 Safe Handoff Reporting

Customer-safe v0.6 reporting may cite:

- `artifacts/service-governance-audit-v0.6.json`
- `artifacts/service-governance-audit-v0.6.md`
- `artifacts/safe-handoff-package-v0.6/safe_handoff_manifest.json`
- `artifacts/safe-handoff-package-v0.6/safe_handoff_summary.md`
- `artifacts/safe-handoff-package-v0.6/customer_boundary_statement.md`

Reports must state that the service material is synthetic technical review
output. It contains no PHI, no raw DICOM, no real customer name, and no real
hospital name. It is not clinical validation, not regulatory approval, not
certification, and not a compliance certificate.
