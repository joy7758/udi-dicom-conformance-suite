# Operator Manual v0.4

This service workflow supports synthetic sample validation review and pilot
handoff preparation.

## Workflow

1. Discovery: confirm scope, synthetic-only status, and review goal.
2. Intake: accept only approved synthetic or de-identified metadata summaries.
3. Validation: run public validator summaries and private partner-safe checks.
4. Report: write review findings with safe boundary language.
5. Delivery: build a delivery package and audit trail.
6. Pilot handoff: provide checklist, scope, success criteria, and boundary
   statement.

## Stop Conditions

Stop immediately if suspected PHI appears. Do not continue until the artifact is
removed or routed through a separate approved handling path.

Stop if a raw DICOM original is supplied. Raw DICOM originals are not included in
delivery packages.

Do not write conclusions as clinical validation, regulatory approval, or
certification. Outputs are review/report materials only.

## v0.5 Synthetic Customer Dry Run

Before customer-facing dry-run discussion:

```bash
python scripts/run_synthetic_customer_dry_run.py
python scripts/check_synthetic_customer_dry_run.py artifacts/synthetic-customer-dry-run
python scripts/audit_service_language.py
```

Use only synthetic technical review outputs. Do not accept PHI, raw DICOM, real
clinical reports, real customer names, real hospital names, clinical validation
wording, regulatory approval wording, or certification wording.

## v0.6 Feedback and Safe Handoff Gate

Before any customer review or pilot handoff conversation, run:

```bash
python scripts/audit_service_governance.py
python scripts/build_safe_handoff_package.py
python scripts/check_safe_handoff_package.py artifacts/safe-handoff-package-v0.6
```

Use `docs/customer-feedback-intake-v0.6.md` and
`docs/customer-feedback-triage.md` to classify feedback. Use
`docs/customer-feedback-safe-response.md` when responding to boundary concerns.

Stop and mark out of scope if a request asks for PHI handling, raw DICOM
delivery, clinical validation, regulatory approval, certification, real hospital
deployment approval, or real customer approval. Real cooperation requires NDA
and de-identification review before any sample discussion proceeds.
