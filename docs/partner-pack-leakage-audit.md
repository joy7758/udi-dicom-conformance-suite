# Partner Pack Leakage Audit

`tools/audit_partner_pack_leakage.py` checks generated partner-pack outputs
before a partner-facing package is shared.

Checks:

- no `cases/private` paths
- no private-only markers
- no raw DICOM files
- no PHI fields such as PatientName, PatientID, AccessionNumber, BirthDate, or
  MRN
- no unbounded clinical diagnosis, regulatory approval, or certification
  language

Boundary phrases such as "not clinical validation", "not regulatory approval",
and "not certification" are allowed because they preserve the required review
boundary.

Run:

```bash
python tools/build_partner_pack.py
python tools/audit_partner_pack_leakage.py
```
