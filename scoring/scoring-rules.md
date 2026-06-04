# Scoring Rules

Case weight, pass/warn/fail outcome, primary error correctness, secondary warning
tolerance, deterministic output, and regression policy are tracked per case.

Score bands: Ready for sample validation, Needs mapping review, Not ready.


## v0.2 Checks

- `trace_id_consistency`: workflow trace id must match between manifest, provenance, and registry fixture when present.
- `fdo_mapping_consistency`: optional FDO-style mapping metadata must remain internally consistent with v0.2 profile identifiers.
- Synthetic-data, no-PHI, and offline-fixture-first constraints remain mandatory.


## v0.3 Scoring

Scoring includes golden regression stability, partner pack readiness, profile version compatibility, trace_id consistency, FDO mapping consistency, and registry fixture reproducibility. Partner pack readiness requires synthetic_data=true, no_phi=true, no private paths, and expected_primary_error_code present.
## v0.4 Partner Pack Readiness

Scorecards must include:

- leakage audit status
- release asset hash status
- partner pack readiness
- private regression baseline status
- profile compatibility summary

Any leakage audit failure is a release blocker. Any missing SHA256SUMS entry is
a release blocker. These scores support synthetic partner review only and are
not clinical validation, regulatory approval, or certification.

## v0.5 Partner Dry Run Readiness

Scoring now includes:

- `partner_dry_run_readiness`: generated package exists, partner-safe case count
  is at least 25, and `check_partner_dry_run_package.py` passes.
- `evidence_boundary_audit_status`: `audit_evidence_boundary.py` passes and
  writes JSON and Markdown artifacts.
- `partner_question_bank_status`: v0.5 question bank and safe-answer boundary
  documents exist.

Severity model:

- Critical: PHI, raw DICOM file, private case path in partner output, or unsafe
  clinical/regulatory/certification upgrade language.
- Major: missing dry-run package, stale case index, missing boundary audit, or
  missing partner question bank.
- Minor: incomplete reviewer notes that do not change the safety boundary.

## v0.6 Governance Scoring

Scoring includes partner feedback intake readiness, private asset governance
audit status, private case lifecycle documentation, synthetic case authoring
guide status, and public paper support boundary status.

Any private case leakage into partner-facing outputs, PHI marker, raw DICOM
asset, real vendor confidential rule, clinical validation claim, regulatory
approval claim, or certification claim is a critical blocker.
