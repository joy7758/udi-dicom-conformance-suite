# Severity Model

Definitions: fail, warn, info, blocked, not_applicable.

## v0.2 Severity

Trace id mismatch and FDO mapping mismatch are fail when deterministic validation can prove inconsistency; ambiguous alias cases are warn/manual review.


## v0.3 Severity

Golden regression drift is fail for release candidates. Partner pack private leakage is blocked. Profile compatibility gaps are warn unless they break deterministic validation.
