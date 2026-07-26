"""Incremental historical poller for licensed CME/Globex bars through Databento.

Why this exists
---------------
Some workflows do not require a persistent live WebSocket stream. For those
cases, this poller repeatedly asks the historical API for a small recent range,
merges the returned closed bars into DAL CSV files, and lets MT5 consume those
files through EXP0015 EXTERNAL_CSV mode.

This is not a substitute for a true live feed. It is a near-live backfill/polling
mode with a configurable delay to avoid requesting an incomplete current bar.
It must be used with legal provider credentials and within provider/exchange
entitlements, limits, and cost rules.
"""
from __future__ import annotations

import argparse
import os
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from adapters.legacy.market_data.cme_bridge.dal_bar_store import latest_bar_time, merge_bars
from adapters.legacy.market_data.cme_bridge.providers.databento_provider import (
    DatabentoConfig,
    DatabentoSymbol,
    dataframe_to_bars,
    load_config,
    require_databento,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def fmt_dt(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def request_symbol_range(client: Any, config: DatabentoConfig, spec: DatabentoSymbol, start: datetime, end: datetime) -> int:
    if end <= start:
        print(f"skip {spec.alias}: empty range start={fmt_dt(start)} end={fmt_dt(end)}")
        return 0
    print(f"historical poll {spec.alias} <- {spec.databento_symbol} {fmt_dt(start)}..{fmt_dt(end)}")
    data = client.timeseries.get_range(
        dataset=config.dataset,
        schema=config.schema,
        symbols=spec.databento_symbol,
        stype_in=config.stype_in,
        start=fmt_dt(start),
        end=fmt_dt(end),
    )
    df = data.to_df()
    bars = dataframe_to_bars(spec.alias, df)
    out = config.output_dir / f"{spec.alias}_M1.csv"
    total = merge_bars(out, bars, max_rows=config.max_rows)
    print(f"merged {len(bars)} new/overlap bars; file_rows={total} -> {out}")
    return len(bars)


def compute_start(path: Path, *, now: datetime, overlap_minutes: int, bootstrap_minutes: int) -> datetime:
    last = latest_bar_time(path)
    if last is None:
        return now - timedelta(minutes=bootstrap_minutes)
    return last - timedelta(minutes=overlap_minutes)


def poll_once(
    config: DatabentoConfig,
    *,
    key: str | None,
    overlap_minutes: int,
    bootstrap_minutes: int,
    end_delay_seconds: int,
) -> int:
    db = require_databento()
    client = db.Historical(key=key) if key else db.Historical()
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # Delay the end time so the provider has a chance to finalize the latest
    # 1-minute OHLCV bar. Increase this if your feed often returns partial bars.
    end = utc_now() - timedelta(seconds=end_delay_seconds)
    total_bars = 0
    for spec in config.symbols:
        out = config.output_dir / f"{spec.alias}_M1.csv"
        start = compute_start(out, now=end, overlap_minutes=overlap_minutes, bootstrap_minutes=bootstrap_minutes)
        try:
            total_bars += request_symbol_range(client, config, spec, start=start, end=end)
        except KeyboardInterrupt:
            raise
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR historical poll failed alias={spec.alias}: {exc}", file=sys.stderr)
    return total_bars


def run_forever(
    config: DatabentoConfig,
    *,
    key: str | None,
    interval_seconds: int,
    overlap_minutes: int,
    bootstrap_minutes: int,
    end_delay_seconds: int,
) -> None:
    stopping = False

    def handle_signal(_sig: int, _frame: Any) -> None:
        nonlocal stopping
        stopping = True
        print("stopping historical poller...")

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while not stopping:
        started = time.time()
        print("\n=== DAL CME historical poll", datetime.now(timezone.utc).isoformat(), "===")
        poll_once(
            config,
            key=key,
            overlap_minutes=overlap_minutes,
            bootstrap_minutes=bootstrap_minutes,
            end_delay_seconds=end_delay_seconds,
        )
        elapsed = time.time() - started
        sleep_for = max(1.0, float(interval_seconds) - elapsed)
        print(f"poll complete elapsed={elapsed:.1f}s next_in={sleep_for:.1f}s")
        end_at = time.time() + sleep_for
        while not stopping and time.time() < end_at:
            time.sleep(min(1.0, end_at - time.time()))


def main() -> None:
    parser = argparse.ArgumentParser(description="DAL Databento incremental historical poller")
    parser.add_argument("--config", default="adapters/legacy/market_data/cme_bridge/configs/databento_es_nq.example.json")
    parser.add_argument("--key", default=os.getenv("DATABENTO_API_KEY"), help="defaults to DATABENTO_API_KEY")
    parser.add_argument("--interval-seconds", type=int, default=300, help="poll cadence; 300 = every 5 minutes")
    parser.add_argument("--overlap-minutes", type=int, default=10, help="overlap previous data so late/revised bars are replaced")
    parser.add_argument("--bootstrap-minutes", type=int, default=180, help="initial lookback if output CSV does not exist")
    parser.add_argument("--end-delay-seconds", type=int, default=90, help="avoid incomplete most-recent bar")
    parser.add_argument("--once", action="store_true", help="run one incremental poll and exit")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    if args.once:
        poll_once(
            config,
            key=args.key,
            overlap_minutes=args.overlap_minutes,
            bootstrap_minutes=args.bootstrap_minutes,
            end_delay_seconds=args.end_delay_seconds,
        )
        return
    run_forever(
        config,
        key=args.key,
        interval_seconds=args.interval_seconds,
        overlap_minutes=args.overlap_minutes,
        bootstrap_minutes=args.bootstrap_minutes,
        end_delay_seconds=args.end_delay_seconds,
    )


if __name__ == "__main__":
    main()
