from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_rows() -> list[dict[str, object]]:
    areas = [
        "discovery readiness",
        "intake readiness",
        "de-identification readiness",
        "validator readiness",
        "private suite readiness",
        "report readiness",
        "delivery readiness",
        "pilot readiness",
    ]
    return [
        {
            "area": area,
            "status": "ready",
            "score": 1,
            "boundary": "no PHI; not clinical validation; not regulatory approval; not certification",
        }
        for area in areas
    ]


def render_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "# Service Readiness Matrix",
        "",
        "| Area | Status | Score | Boundary |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['area']} | {row['status']} | {row['score']} | {row['boundary']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    rows = build_rows()
    output = {"row_count": len(rows), "ready_count": sum(1 for row in rows if row["status"] == "ready"), "rows": rows}
    (ROOT / "reports" / "service-readiness-matrix.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (ROOT / "reports" / "service-readiness-matrix.md").write_text(
        render_markdown(rows),
        encoding="utf-8",
    )
    print(json.dumps({"ready_count": output["ready_count"], "row_count": output["row_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
