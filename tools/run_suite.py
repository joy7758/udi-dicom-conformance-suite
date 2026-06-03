from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-validator-path", required=True)
    parser.add_argument("--cases", default="cases")
    parser.add_argument("--out", default="suite_result.json")
    args = parser.parse_args()
    result = {
        "public_validator_path": args.public_validator_path,
        "cases": args.cases,
        "status": "planned",
        "note": "Skeleton runner; integrate with public CLI in controlled environment.",
    }
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.out)


if __name__ == "__main__":
    main()
