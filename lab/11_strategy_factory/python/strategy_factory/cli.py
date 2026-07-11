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
from .scaffold_v2 import scaffold_strategy_v2
from .optimization import compile_strategy_plan, load_plan_spec
from .plugins import PluginRegistry, register_builtins_from_spec
from .serving import benchmark, build_reference_fast_engine
from .contracts import AnatomyEvent, Direction
from datetime import datetime, timezone


def _json_print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))



def command_scaffold_v2(args: argparse.Namespace) -> int:
    root = scaffold_strategy_v2(args.strategy_id, args.output_root, force=args.force)
    _json_print({"ok": True, "strategy_root": str(root), "version": "v2"})
    return 0

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


def _load_json_object(path: str | None, default):
    if not path:
        return default
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def command_compile_v2(args: argparse.Namespace) -> int:
    spec = load_plan_spec(args.spec)
    registry = PluginRegistry()
    register_builtins_from_spec(spec, registry)
    plan = compile_strategy_plan(spec, registry)
    description = dict(plan.describe())
    if args.output:
        Path(args.output).write_text(json.dumps(description, indent=2, default=str), encoding="utf-8")
    _json_print(description)
    return 0


def _event_from_payload(payload):
    def dt(name, default):
        raw = payload.get(name, default)
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    direction = Direction(str(payload.get("direction", "long")))
    reference = float(payload.get("reference_price", 100.0))
    invalidation = payload.get("invalidation_price")
    if invalidation is None:
        invalidation = reference - 1.0 if direction == Direction.LONG else reference + 1.0
    event = AnatomyEvent(
        event_id=str(payload.get("event_id", "cli_event")),
        strategy_id=str(payload.get("strategy_id", "cli_strategy")),
        strategy_version=str(payload.get("strategy_version", "2.0.0")),
        symbol=str(payload.get("symbol", "TEST")),
        direction=direction,
        event_time_utc=dt("event_time_utc", now.isoformat()),
        known_time_utc=dt("known_time_utc", now.isoformat()),
        confirmation_time_utc=dt("confirmation_time_utc", now.isoformat()),
        reference_price=reference,
        invalidation_price=float(invalidation),
        reference_symbol=payload.get("reference_symbol"),
        timeframe=payload.get("timeframe"),
        session=payload.get("session"),
        market_event_cluster_id=payload.get("market_event_cluster_id", "cli_cluster"),
    )
    event.validate()
    return event


def command_decide_v2(args: argparse.Namespace) -> int:
    spec = load_plan_spec(args.spec)
    engine = build_reference_fast_engine(spec)
    event_payload = _load_json_object(args.event_json, {})
    market_state = _load_json_object(args.market_state_json, {
        "confirmation_close": 100.2, "atr": 1.0, "reference_extreme": 99.0,
        "divergence_strength": 1.0, "volatility_regime": 1.0, "spread_r": 0.02,
        "hook_quality": 0.8, "f_count": 3, "zone_width_atr": 0.4, "free_path_atr": 3.0
    })
    event = _event_from_payload(event_payload)
    envelope = engine.decide(event, market_state, event.confirmation_time_utc, state_generation=1)
    _json_print({
        "status": envelope.status.value,
        "selected_candidate": None if envelope.selected_candidate is None else envelope.selected_candidate.candidate_id,
        "reason_codes": envelope.reason_codes,
        "scores": [score.__dict__ if hasattr(score, "__dict__") else {name: getattr(score, name) for name in score.__slots__} for score in envelope.scores],
        "latency_ns": envelope.latency_ns,
        "diagnostics": envelope.diagnostics,
        "plan_hash": envelope.plan_hash,
    })
    return 0


def command_benchmark_v2(args: argparse.Namespace) -> int:
    spec = load_plan_spec(args.spec)
    event_payload = _load_json_object(args.event_json, {})
    market_state = _load_json_object(args.market_state_json, {
        "confirmation_close": 100.2, "atr": 1.0, "reference_extreme": 99.0,
        "divergence_strength": 1.0, "volatility_regime": 1.0, "spread_r": 0.02,
        "hook_quality": 0.8, "f_count": 3, "zone_width_atr": 0.4, "free_path_atr": 3.0
    })
    counter = {"value": 0}
    engine = build_reference_fast_engine(spec)
    def call():
        counter["value"] += 1
        payload = dict(event_payload)
        payload["event_id"] = f"bench_{counter['value']}"
        event = _event_from_payload(payload)
        return engine.decide(event, market_state, event.confirmation_time_utc, state_generation=1)
    result = benchmark(call, warmup=args.warmup, iterations=args.iterations)
    _json_print(result)
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="strategy-factory")
    sub = parser.add_subparsers(dest="command", required=True)

    scaffold = sub.add_parser("scaffold", help="generate a minimal new-anatomy plugin packet")
    scaffold.add_argument("strategy_id")
    scaffold.add_argument("--output-root", default="lab/03_experiments")
    scaffold.add_argument("--force", action="store_true")
    scaffold.set_defaults(func=command_scaffold)

    scaffold_v2 = sub.add_parser("scaffold-v2", help="generate a V2 anatomy plugin and compiled-plan packet")
    scaffold_v2.add_argument("strategy_id")
    scaffold_v2.add_argument("--output-root", default="lab/03_experiments")
    scaffold_v2.add_argument("--force", action="store_true")
    scaffold_v2.set_defaults(func=command_scaffold_v2)

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

    compile_v2 = sub.add_parser("compile-v2", help="compile and inspect a V2 low-latency strategy plan")
    compile_v2.add_argument("spec")
    compile_v2.add_argument("--output")
    compile_v2.set_defaults(func=command_compile_v2)

    decide_v2 = sub.add_parser("decide-v2", help="run one reference V2 context-to-decision request")
    decide_v2.add_argument("spec")
    decide_v2.add_argument("--event-json")
    decide_v2.add_argument("--market-state-json")
    decide_v2.set_defaults(func=command_decide_v2)

    benchmark_v2 = sub.add_parser("benchmark-v2", help="benchmark the reference V2 decision path")
    benchmark_v2.add_argument("spec")
    benchmark_v2.add_argument("--event-json")
    benchmark_v2.add_argument("--market-state-json")
    benchmark_v2.add_argument("--warmup", type=int, default=20)
    benchmark_v2.add_argument("--iterations", type=int, default=100)
    benchmark_v2.set_defaults(func=command_benchmark_v2)
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
