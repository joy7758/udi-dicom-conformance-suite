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
