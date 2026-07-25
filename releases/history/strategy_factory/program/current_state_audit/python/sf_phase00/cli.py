from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audit import AuditConfig, run_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit a Decision Alpha Lab repository for Strategy Factory Phase 00.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-pytest", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = run_audit(
        args.repo_root,
        args.output,
        AuditConfig(run_pytest=not args.skip_pytest),
    )
    print(json.dumps(result.summary, indent=2, sort_keys=True))
    return 0 if result.summary["phase_gate_status"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
