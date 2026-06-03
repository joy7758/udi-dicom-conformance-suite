from __future__ import annotations

import argparse
from pathlib import Path

TERMS = [
    "PatientName",
    "PatientID",
    "AccessionNumber",
    "BirthDate",
    "Address",
    "Phone",
    "Email",
    "MRN",
]
SKIP = {".git", "__pycache__"}


def should_scan(path: Path) -> bool:
    if any(part in SKIP for part in path.parts):
        return False
    if path.name == "redact_check.py":
        return False
    return path.suffix.lower() in {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    root = Path(args.path)
    hits = []
    for path in root.rglob("*"):
        if path.is_file() and should_scan(path):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for term in TERMS:
                if term in text:
                    hits.append(f"{path}:{term}")
    if hits:
        print("\n".join(hits))
        raise SystemExit(1)
    print("redact_check=pass")


if __name__ == "__main__":
    main()
