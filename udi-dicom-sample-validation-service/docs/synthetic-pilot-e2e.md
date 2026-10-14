# Synthetic Pilot E2E

`scripts/run_synthetic_pilot_e2e.py` builds a complete synthetic pilot workspace
for service review. It uses synthetic summaries and existing generated service
artifacts.

Run:

```bash
python scripts/run_synthetic_pilot_e2e.py
python scripts/check_synthetic_pilot_outputs.py artifacts/synthetic-pilot-e2e
```

Outputs:

- `artifacts/synthetic-pilot-e2e/summary.json`
- `artifacts/synthetic-pilot-e2e/summary.md`

Boundary:

- synthetic-only
- no PHI
- no raw DICOM
- not clinical validation
- not regulatory approval
- not certification
