from __future__ import annotations

import argparse
import json
from pathlib import Path

from .baseline import verify_repository_bytes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="lcm-01-baseline-verify")
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args(argv)
    result = verify_repository_bytes(args.repo_root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
