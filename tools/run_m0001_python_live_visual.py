from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.export_m0001_to_mql import (
    DataFrameEngine,
    _Timeframe,
    default_output_path,
    load_cached_candles,
)
from lab.core.CP0001_structural_nodes.detectors.L_Rule import LRuleNodeDetector
from lab.core.CP0001_structural_nodes.metrics.M0001_rtv import (
    RTVConfig,
    build_visual_rows,
    compute_rtv_events,
    random_reference_points,
    reference_points_from_lrule_nodes,
    write_visual_csv,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Continuously run the Python single-source M0001 engine and export "
            "its visual contract for MT5. MQL only draws this output."
        )
    )
    parser.add_argument("--symbol", default="GOLD")
    parser.add_argument("--timeframe", default="M15")
    parser.add_argument("--bars", type=int, default=1200)
    parser.add_argument("--L", type=int, default=5)
    parser.add_argument("--zone-ratio", type=float, default=0.9)
    parser.add_argument("--exit-gap", type=int, default=6)
    parser.add_argument("--mode", choices=["hunt", "touch"], default="hunt")
    parser.add_argument("--random", action="store_true")
    parser.add_argument("--random-count", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--terminal-files-output", default=None, help="Optional absolute MT5 MQL5/Files output path.")
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    output = Path(args.output) if args.output else default_output_path(args.symbol, args.timeframe)

    while True:
        try:
            rows, stats = build_contract(args)
            output_path = write_visual_csv(output, rows)

            terminal_path = None
            if args.terminal_files_output:
                terminal_path = Path(args.terminal_files_output)
                terminal_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(output_path, terminal_path)

            print(
                "PYTHON M0001 LIVE VISUAL | "
                f"symbol={args.symbol} timeframe={args.timeframe} bars={stats['bars']} "
                f"nodes={stats['actual_nodes']} events={stats['actual_events']} "
                f"rows={len(rows)} output={output_path}"
                + (f" terminal={terminal_path}" if terminal_path else "")
            )
        except Exception as exc:
            print(f"PYTHON M0001 LIVE VISUAL ERROR | {type(exc).__name__}: {exc}", file=sys.stderr)

        if args.once:
            break

        time.sleep(max(0.25, float(args.interval)))

    return 0


def build_contract(args) -> tuple[list[dict], dict]:
    candles = load_cached_candles(args.symbol, args.timeframe, args.bars)

    engine = DataFrameEngine(candles)
    detector = LRuleNodeDetector(engine=engine, L=args.L)
    nodes = detector.detect(args.symbol, _Timeframe(args.timeframe))

    config = RTVConfig(
        L=args.L,
        zone_ratio=args.zone_ratio,
        exit_gap=args.exit_gap,
        consumption_mode=args.mode,
    )

    refs = reference_points_from_lrule_nodes(nodes, candles, args.L)
    events = compute_rtv_events(candles, refs, config)

    all_refs = list(refs)
    all_events = list(events)

    if args.random:
        count = args.random_count or max(1, len(refs))
        rnd_refs = random_reference_points(candles, count=count, L=args.L, seed=args.seed)
        rnd_events = compute_rtv_events(candles, rnd_refs, config)
        all_refs.extend(rnd_refs)
        all_events.extend(rnd_events)

    rows = build_visual_rows(all_refs, all_events, candles_df=candles, config=config)
    stats = {
        "bars": len(candles),
        "actual_nodes": len(refs),
        "actual_events": len(events),
    }
    return rows, stats


if __name__ == "__main__":
    raise SystemExit(main())
