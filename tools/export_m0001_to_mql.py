from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lab.core.CP0001_structural_nodes.detectors.L_Rule import LRuleNodeDetector
from lab.core.CP0001_structural_nodes.metrics.M0001_rtv import (
    RTVConfig,
    build_visual_rows,
    compute_rtv_events,
    random_reference_points,
    reference_points_from_lrule_nodes,
    write_visual_csv,
)
from lab.core.CP0001_structural_nodes.metrics.M0001_rtv.time_utils import normalize_ohlc, read_parquet_compat


class DataFrameEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_df(self, symbol, timeframe):
        return self.df.copy()


def main() -> int:
    parser = argparse.ArgumentParser(description="Export M0001 visual contract for the MT5/MQL5 chart visualizer.")
    parser.add_argument("--symbol", default="GOLD")
    parser.add_argument("--timeframe", default="M15")
    parser.add_argument("--bars", type=int, default=5000)
    parser.add_argument("--L", type=int, default=5)
    parser.add_argument("--zone-ratio", type=float, default=0.9)
    parser.add_argument("--exit-gap", type=int, default=6)
    parser.add_argument("--mode", choices=["hunt", "touch"], default="hunt")
    parser.add_argument("--random", action="store_true", help="Add random-baseline objects to the same visual file.")
    parser.add_argument("--random-count", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

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
    output = Path(args.output) if args.output else default_output_path(args.symbol, args.timeframe)
    output = write_visual_csv(output, rows)

    actual_events = [event for event in all_events if event.baseline_kind == "actual"]
    random_events = [event for event in all_events if event.baseline_kind == "random"]
    print(
        "M0001 MQL EXPORT | "
        f"symbol={args.symbol} timeframe={args.timeframe} bars={len(candles)} "
        f"actual_refs={len(refs)} actual_events={len(actual_events)} "
        f"random_events={len(random_events)} rows={len(rows)} output={output}"
    )
    return 0


def load_cached_candles(symbol: str, timeframe: str, bars: int) -> pd.DataFrame:
    folder = PROJECT_ROOT / "lab" / "cache_data" / symbol / timeframe
    candidates = [
        folder / f"{symbol}_{timeframe}.parquet",
        folder / "data.parquet",
    ]
    if folder.exists():
        for extra in sorted(folder.glob("*.parquet")):
            if extra not in candidates:
                candidates.append(extra)

    loaded: list[pd.DataFrame] = []
    for path in candidates:
        if not path.exists():
            continue
        try:
            df = normalize_ohlc(read_parquet_compat(path))
            loaded.append(df)
        except Exception as exc:
            print(f"warning: skipped {path}: {exc}", file=sys.stderr)

    if not loaded:
        raise FileNotFoundError(f"No cached candles found for {symbol} {timeframe} under {folder}")

    df = max(loaded, key=len).tail(int(bars)).reset_index(drop=True)
    return df


def default_output_path(symbol: str, timeframe: str) -> Path:
    return PROJECT_ROOT / "mql5" / "Files" / "DecisionAlphaLab" / "M0001" / f"{symbol}_{timeframe}_visual.csv"


class _Timeframe:
    def __init__(self, name: str):
        self.name = name


if __name__ == "__main__":
    raise SystemExit(main())
