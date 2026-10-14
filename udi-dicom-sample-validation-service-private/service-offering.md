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

## v0.5 Synthetic Customer Dry Run

The v0.5 service material supports a synthetic customer dry run for technical
review. It generates a customer-safe report, handoff checklist, and service
language audit. This is not a real customer pilot, not clinical validation, not
regulatory approval, not certification, and not hospital deployment.

## v0.6 Service Feedback Governance

The v0.6 service material adds customer feedback intake, service governance
audit, safe handoff package generation, and public-paper support boundary
documents. These materials are for synthetic technical review and controlled
partner discussion only.

Customer feedback is triaged as discovery question, sample intake question,
de-identification concern, validation report question, delivery package
question, pilot handoff question, or out-of-scope request. Real cooperation
requires NDA and de-identification review before any transfer is considered.

Safe handoff outputs remain summaries, receipts, generated reports, audit
trails, and boundary statements. They include no PHI, no raw DICOM, no real
clinical report, no real customer name, and no real hospital name. The service
does not provide clinical validation, regulatory approval, certification, or a
compliance certificate.

## v0.7 Service Feedback Prep

The v0.7 service material prepares customer feedback and safe handoff review
after v0.6. It confirms that synthetic customer dry-run outputs, service
governance audits, and safe handoff packages remain customer-safe before any
new conversation.

v0.7 does not authorize real sample transfer, PHI intake, raw DICOM delivery,
clinical validation, regulatory approval, certification, real hospital
deployment, or customer approval. Real cooperation still requires NDA and
de-identification review before any sample-specific workflow.
