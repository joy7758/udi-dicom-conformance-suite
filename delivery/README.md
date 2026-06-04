# Delivery Package

Generated delivery packages contain summaries, receipts, reports, redaction
logs, and manifests. They must not contain original DICOM files, patient reports,
raw clinical reports, private conformance cases, customer confidential artifacts,
or PHI.

Boundary: not clinical validation, not regulatory approval, not certification.
## v0.4 Delivery Audit Trail

Run:

```bash
python scripts/build_delivery_audit_trail.py --synthetic-demo
```

The audit trail records generated artifacts and SHA-256 hashes for synthetic
review delivery. It does not include PHI, raw DICOM, clinical validation,
regulatory approval, or certification outputs.

## v0.5 Customer-Safe Delivery

Customer-safe delivery may include synthetic dry run summaries, customer-safe
reports, handoff checklists, delivery audit trail summaries, and service
language audit summaries. It must not include raw DICOM, PHI, real clinical
reports, real customer names, real hospital names, compliance certificate
language, regulatory clearance, or certification.
