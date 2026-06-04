# Evidence Boundary Audit v0.5

The evidence boundary audit checks suite text and generated outputs for unsafe
claims or leakage indicators.

Run:

```bash
python tools/audit_evidence_boundary.py
```

Outputs:

- `artifacts/evidence-boundary-audit-v0.5.json`
- `artifacts/evidence-boundary-audit-v0.5.md`

Checks include raw DICOM extension detection, PHI field indicators, private
case paths in partner outputs, real customer or real hospital name indicators,
Device UID confused with UDI-DI, and clinical diagnosis/regulatory
approval/certification upgrade language.

Safe boundary statements such as "not clinical validation", "not regulatory
approval", and "not certification" are allowed because they preserve the review
boundary.

