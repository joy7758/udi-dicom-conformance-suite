# Validation Runbook

Run public CLI and aggregate receipts.


## v0.2 Commands

Use `scripts/run_validation_batch.py --profile-version v0.2.0 --out batch_summary_v0.2.json` and package delivery with `delivery_manifest_v0.2.json`.


## v0.3 Runbook

Run service readiness matrix, pilot kit generator, delivery package builder, and delivery package checker before sending any partner-facing material.
## v0.4 Synthetic Pilot Run

Run:

```bash
python scripts/run_synthetic_pilot_e2e.py
python scripts/check_synthetic_pilot_outputs.py artifacts/synthetic-pilot-e2e
python scripts/build_delivery_audit_trail.py --synthetic-demo
```

Stop if suspected PHI or raw DICOM originals appear. All conclusions must remain
review/report conclusions, not clinical validation, regulatory approval, or
certification.

## v0.5 Dry Run Gate

For synthetic customer dry runs, execute the customer dry run script, dry run
checker, delivery package checker, redaction check, and service language audit.
Only customer-safe summaries and reports may move to handoff.

## v0.6 Governance and Handoff Gate

Run:

```bash
python scripts/audit_service_governance.py
python scripts/build_safe_handoff_package.py
python scripts/check_safe_handoff_package.py artifacts/safe-handoff-package-v0.6
```

Do not proceed if the governance audit reports PHI markers, raw DICOM files,
clinical validation wording, regulatory approval wording, certification wording,
customer unsafe promises, hospital deployment overclaims, missing NDA language,
or missing de-identification language.

Validation results remain technical review findings. They are not clinical
validation, not regulatory approval, not certification, and not medical
decision support.
