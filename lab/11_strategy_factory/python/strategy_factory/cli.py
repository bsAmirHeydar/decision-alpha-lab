"""Command-line interface for the shared Strategy Factory."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

import pandas as pd

from .audit import audit_bar_data, audit_model_dataset
from .manifest import load_manifest
from .statistics import grouped_summary, summarize
from .scaffold import scaffold_strategy


def _json_print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def command_validate_manifest(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    _json_print(
        {
            "valid": True,
            "strategy_id": manifest.strategy_id,
            "version": manifest.version,
            "status": manifest.status,
            "manifest_hash": manifest.manifest_hash,
        }
    )
    return 0


def command_audit_bars(args: argparse.Namespace) -> int:
    path = Path(args.input)
    frame = pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
    report = audit_bar_data(frame)
    _json_print(report.to_dict())
    return 0 if report.passed else 2


def command_audit_dataset(args: argparse.Namespace) -> int:
    path = Path(args.input)
    frame = pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
    features = [item.strip() for item in args.features.split(",") if item.strip()]
    report = audit_model_dataset(frame, feature_columns=features)
    _json_print(report.to_dict())
    return 0 if report.passed else 2


def command_stats(args: argparse.Namespace) -> int:
    path = Path(args.input)
    frame = pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
    if args.group_by:
        groups = [item.strip() for item in args.group_by.split(",") if item.strip()]
        result = grouped_summary(frame, groups, return_col=args.return_col, minimum_samples=args.minimum_samples)
        if args.output:
            result.to_csv(args.output, index=False)
        else:
            print(result.to_string(index=False))
    else:
        _json_print(summarize(frame, return_col=args.return_col).to_dict())
    return 0



def command_scaffold(args: argparse.Namespace) -> int:
    root = scaffold_strategy(args.strategy_id, args.output_root, force=args.force)
    _json_print({"ok": True, "strategy_root": str(root)})
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="strategy-factory")
    sub = parser.add_subparsers(dest="command", required=True)

    scaffold = sub.add_parser("scaffold", help="generate a minimal new-anatomy plugin packet")
    scaffold.add_argument("strategy_id")
    scaffold.add_argument("--output-root", default="lab/03_experiments")
    scaffold.add_argument("--force", action="store_true")
    scaffold.set_defaults(func=command_scaffold)

    validate = sub.add_parser("validate-manifest", help="validate a Strategy Factory manifest")
    validate.add_argument("manifest")
    validate.set_defaults(func=command_validate_manifest)

    audit_bars = sub.add_parser("audit-bars", help="audit OHLC/bar data")
    audit_bars.add_argument("input")
    audit_bars.set_defaults(func=command_audit_bars)

    audit_dataset = sub.add_parser("audit-dataset", help="audit a candidate-level model dataset")
    audit_dataset.add_argument("input")
    audit_dataset.add_argument("--features", required=True, help="comma-separated feature columns")
    audit_dataset.set_defaults(func=command_audit_dataset)

    stats = sub.add_parser("stats", help="produce standard strategy statistics")
    stats.add_argument("input")
    stats.add_argument("--return-col", default="net_r")
    stats.add_argument("--group-by", default="")
    stats.add_argument("--minimum-samples", type=int, default=1)
    stats.add_argument("--output")
    stats.set_defaults(func=command_stats)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        _json_print({"ok": False, "error": type(exc).__name__, "message": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
