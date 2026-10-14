# Delivery Audit Trail

`scripts/build_delivery_audit_trail.py --synthetic-demo` creates a deterministic
v0.4 delivery audit trail at
`delivery/generated/delivery_audit_trail_v0.4.json`.

The audit trail records:

- delivery id
- creation timestamp
- service version
- validator version
- suite version
- source artifacts
- generated artifacts
- SHA-256 hashes
- redaction check status
- forbidden asset check status
- boundary statement
- reviewer notes

The audit trail does not package raw DICOM, does not include PHI, does not use
real sample paths, and does not create clinical validation, regulatory approval,
or certification claims.
