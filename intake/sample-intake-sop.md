# Sample Intake SOP

NDA, no PHI, de-identification review, custody log, acceptance gate.


## v0.2 Intake

Record trace_id and provenance in the intake log. Reject any packet that attempts to use v0.2 traceability as certification or regulatory approval.


## v0.3 Intake for Delivery

Run redact check before package generation. Delivery package inputs must be summaries, receipts, redaction logs, and reports, not raw DICOM.

## v0.6 Feedback Intake Gate

Use `docs/customer-feedback-intake-v0.6.md` for customer review intake and
`docs/customer-feedback-scope-policy.md` for out-of-scope routing.

Accepted feedback categories are discovery question, sample intake question,
de-identification concern, validation report question, delivery package
question, pilot handoff question, and out-of-scope request.

Reject PHI, raw DICOM delivery, real clinical reports, real customer names, real
hospital names, clinical validation requests, regulatory approval requests, and
certification requests. Real cooperation requires NDA and de-identification
review before any sample-specific workflow is discussed.
