# Service Offering

Service name: UDI-DICOM Evidence Packet Review.

Service target: review de-identified equipment metadata and UDI evidence packets.

Inputs: metadata extracts, manifest candidates, registry context, and evidence
artifact summaries.

Outputs: receipts, reports, remediation notes, and delivery manifest.

Delivery cycle: placeholder to be scoped per pilot.

Out of scope: clinical validation, regulatory approval, certification, medical
decision support, PHI handling, and original DICOM archival.

Customer responsibilities: de-identification, chain-of-custody, data owner
approval, and vendor coordination.

Data boundary: no PHI and no raw DICOM in delivery package.

NDA after flow: discovery, intake, validation, report, remediation review.

Boundary phrase: not clinical validation, not regulatory approval, no PHI, not certification.


## v0.2 Service Scope

Supports public validator v0.2 and private suite v0.2 fields: trace_id, provenance, and optional FDO-style mapping metadata. Boundary phrase: not clinical validation, not regulatory approval, no PHI, not certification.


## v0.3 Delivery Workflow

The v0.3 service can generate a delivery package, pilot kit, and service readiness matrix. Delivery excludes original DICOM files, private conformance cases, customer confidential artifacts, and PHI. trace_id and FDO mapping fields are handled as review metadata only. Registry fixtures remain offline first.
## v0.4 Synthetic Pilot E2E

The service can run a synthetic end-to-end pilot workflow using
`scripts/run_synthetic_pilot_e2e.py`. The workflow builds a delivery package,
pilot kit, redaction check result, delivery package check result, and delivery
audit trail for review.

Boundary: no PHI, no raw DICOM delivery, not clinical validation, not regulatory
approval, not certification.
