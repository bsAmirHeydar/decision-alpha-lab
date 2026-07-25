"""Command-line entry point for FP-I00."""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

from .manifest import build_manifest, write_manifest
from .reporting import write_artifacts
from .scanner import load_json
from .validator import GovernanceValidator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FP-I00 governance baseline and source-control harness")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--policy", default="contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/config/FP_I00_GOVERNANCE_POLICY.v1.json")
    parser.add_argument("--generate", action="store_true", help="regenerate baseline and inventories before validation")
    parser.add_argument("--json", action="store_true", help="print full JSON report")
    args = parser.parse_args(argv)
    repo = Path(args.repo).resolve()
    policy = load_json(repo / args.policy)
    if args.generate:
        manifest = build_manifest(repo, policy)
        write_manifest(repo / policy["baseline_manifest_path"], manifest)
    report = GovernanceValidator(repo, policy).run()
    write_artifacts(repo, policy, report)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"FP-I00 governance: health={report.health.value} checks={report.checks_run} errors={len(report.errors)} warnings={len(report.warnings)}")
        for issue in report.issues:
            print(f"{issue.severity.value}: {issue.code}: {issue.path}: {issue.message}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
