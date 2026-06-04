# Partner Scorecard Template

Partner, scope, score band, findings, next steps.

## v0.2 Fields

Record v0.2 trace id coverage, provenance completeness, FDO-style mapping consistency, and offline registry fixture status.


## v0.3 Partner Pack Readiness

Record partner pack case count, private exclusion confirmation, regression baseline summary, profile compatibility, trace_id consistency, FDO mapping consistency, and registry fixture reproducibility.
## v0.4 Release Readiness

- Leakage audit status: `pass|fail|not_run`
- Release asset hash status: `pass|fail|not_run`
- Partner pack readiness: `ready|hold`
- Private regression baseline status: `current|stale|not_run`
- Profile compatibility summary: `v0.1|v0.2|v0.3-planned`

Boundary: synthetic review only, no PHI, not clinical validation, not regulatory
approval, not certification.

## v0.5 Partner Dry Run

- Partner dry run readiness: `ready|hold`
- Partner-safe case count:
- Evidence boundary audit status: `pass|fail|not_run`
- Partner question bank status: `current|missing`
- Safe answer policy reviewed: `yes|no`
- Device UID != UDI-DI boundary confirmed: `yes|no`
- FDO-style mapping boundary confirmed: `yes|no`

Any `fail`, `hold`, or missing boundary confirmation blocks partner sharing.

## v0.6 Feedback Governance

- Partner feedback category:
- Safe response status:
- Private asset governance audit: `pass|fail|not_run`
- NDA/de-identification gate needed: `yes|no`
- Public paper support boundary reviewed: `yes|no`

Do not include private case content, PHI, raw DICOM, real vendor confidential
rules, clinical validation, regulatory approval, or certification.
