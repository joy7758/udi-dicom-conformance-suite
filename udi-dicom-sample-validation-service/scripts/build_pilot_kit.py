from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "pilot" / "generated"


def main() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    files = {
        "pilot_readiness_checklist.md": "# Pilot Readiness Checklist\n\n- NDA in place\n- no PHI\n- de-identification reviewed\n- not clinical validation\n- not regulatory approval\n- not certification\n- no hospital-level deployment promise\n",
        "pilot_scope_template.md": "# Pilot Scope Template\n\nSynthetic or de-identified metadata review only. No price amount. No hospital-level deployment promise.\n",
        "pilot_success_criteria.md": "# Pilot Success Criteria\n\nDelivery package generated, redaction check pass, trace_id handling reviewed, registry fixture policy followed, no PHI, and no hospital-level deployment promise.\n",
        "pilot_boundary_statement.md": "# Pilot Boundary Statement\n\nThis pilot is not clinical validation, not regulatory approval, not certification, and not hospital-level deployment.\n",
    }
    for name, body in files.items():
        (GENERATED / name).write_text(body, encoding="utf-8")
    print(json.dumps({"generated_files": sorted(files)}, sort_keys=True))


if __name__ == "__main__":
    main()
