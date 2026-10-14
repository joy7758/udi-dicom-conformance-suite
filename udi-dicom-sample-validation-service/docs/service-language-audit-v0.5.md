# Service Language Audit v0.5

The service language audit checks public-facing and operator-facing service
material for unsafe language and delivery risks.

Run:

```bash
python scripts/audit_service_language.py
```

Outputs:

- `artifacts/service-language-audit-v0.5.json`
- `artifacts/service-language-audit-v0.5.md`

Checks cover PHI markers, raw DICOM inclusion risk, clinical/regulatory/
certification upgrade language, customer unsafe claims, hospital deployment
overclaim, pricing overcommitment, and missing boundary phrases.

Safe boundary statements are required: technical review only, no PHI, no raw
DICOM, synthetic demo differs from real cooperation, not clinical validation,
not regulatory approval, and not certification.

