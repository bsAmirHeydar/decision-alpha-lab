from __future__ import annotations

import argparse
from pathlib import Path

from .apply import apply
from .verify import verify


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("apply", "verify"))
    parser.add_argument("--repo-root", default=".")
    arguments = parser.parse_args()
    if arguments.command == "apply":
        apply(Path(arguments.repo_root))
        return 0
    return 0 if verify(Path(arguments.repo_root))["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
