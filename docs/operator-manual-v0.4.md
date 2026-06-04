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
