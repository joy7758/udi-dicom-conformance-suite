# Service Governance Audit v0.6

Run:

```bash
python scripts/audit_service_governance.py
```

Outputs:

- `artifacts/service-governance-audit-v0.6.json`
- `artifacts/service-governance-audit-v0.6.md`

The audit checks PHI markers, raw DICOM risk, clinical/regulatory/certification
upgrade language, customer unsafe promises, hospital deployment overclaim,
required boundary statements, NDA statements, de-identification statements, and
generated artifact safety.

