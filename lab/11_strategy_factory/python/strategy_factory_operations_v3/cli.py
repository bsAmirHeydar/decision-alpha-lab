from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parsing import load_json_object


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a UCE-I19 operations evidence JSON object without granting authority.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = load_json_object(args.path)
    print(json.dumps({"path": str(args.path), "keys": sorted(payload), "authority_granted": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
