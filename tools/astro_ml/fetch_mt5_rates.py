#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir

TF_MAP = {
    "M1": "TIMEFRAME_M1",
    "M2": "TIMEFRAME_M2",
    "M3": "TIMEFRAME_M3",
    "M4": "TIMEFRAME_M4",
    "M5": "TIMEFRAME_M5",
    "M6": "TIMEFRAME_M6",
    "M10": "TIMEFRAME_M10",
    "M12": "TIMEFRAME_M12",
    "M15": "TIMEFRAME_M15",
    "M20": "TIMEFRAME_M20",
    "M30": "TIMEFRAME_M30",
    "H1": "TIMEFRAME_H1",
    "H2": "TIMEFRAME_H2",
    "H3": "TIMEFRAME_H3",
    "H4": "TIMEFRAME_H4",
    "H6": "TIMEFRAME_H6",
    "H8": "TIMEFRAME_H8",
    "H12": "TIMEFRAME_H12",
    "D1": "TIMEFRAME_D1",
}


def parse_dt(s: str) -> datetime:
    s = s.strip().replace(".", "-").replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse datetime: {s}")


def import_mt5():
    try:
        import MetaTrader5 as mt5  # type: ignore
        return mt5
    except Exception as exc:
        raise SystemExit(
            "MetaTrader5 Python package is required for auto rate fetching.\n"
            "Install on Windows with: python -m pip install MetaTrader5\n"
            "MT5 terminal must be installed and logged in."
        ) from exc


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch OHLC rates directly from the local MetaTrader 5 terminal for Astro ML.")
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--timeframe", default="M1", choices=sorted(TF_MAP.keys()))
    ap.add_argument("--from", dest="from_dt", required=True, help="Broker/local terminal time, e.g. 2026-06-22 00:00")
    ap.add_argument("--to", dest="to_dt", required=True, help="Broker/local terminal time, e.g. 2026-06-27 23:59")
    ap.add_argument("--out-csv", default="", help="Absolute path or Common Files relative path.")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--terminal-path", default="", help="Optional terminal64.exe path for mt5.initialize(path=...).")
    ap.add_argument("--login", type=int, default=0)
    ap.add_argument("--password", default="")
    ap.add_argument("--server", default="")
    args = ap.parse_args()

    mt5 = import_mt5()
    init_kwargs = {}
    if args.terminal_path:
        init_kwargs["path"] = args.terminal_path
    if args.login:
        init_kwargs["login"] = args.login
    if args.password:
        init_kwargs["password"] = args.password
    if args.server:
        init_kwargs["server"] = args.server

    if not mt5.initialize(**init_kwargs):
        code, msg = mt5.last_error()
        raise SystemExit(f"mt5.initialize failed: {code} {msg}")

    try:
        tf_attr = TF_MAP[args.timeframe.upper()]
        timeframe = getattr(mt5, tf_attr)
        symbol = args.symbol
        if not mt5.symbol_select(symbol, True):
            code, msg = mt5.last_error()
            raise SystemExit(f"symbol_select failed for {symbol}: {code} {msg}")

        start = parse_dt(args.from_dt)
        end = parse_dt(args.to_dt)
        rates = mt5.copy_rates_range(symbol, timeframe, start, end)
        if rates is None or len(rates) == 0:
            code, msg = mt5.last_error()
            raise SystemExit(f"No rates returned for {symbol} {args.timeframe}: {code} {msg}")

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        # Keep names aligned with astro_ml_core price detection.
        cols = ["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"]
        df = df[[c for c in cols if c in df.columns]].copy()

        common = Path(args.common_files)
        if args.out_csv:
            out = Path(args.out_csv)
            if not out.is_absolute():
                out = common / out
        else:
            safe_from = start.strftime("%Y%m%d")
            safe_to = end.strftime("%Y%m%d")
            out = common / f"astro_ml_prices_{symbol}_{args.timeframe}_{safe_from}_to_{safe_to}.csv"
        ensure_dir(out.parent)
        df.to_csv(out, index=False, encoding="utf-8")

        print(f"MT5_RATES_CSV={out}")
        print(f"ROWS={len(df)}")
        print(f"FIRST_TIME={df['time'].iloc[0]}")
        print(f"LAST_TIME={df['time'].iloc[-1]}")
    finally:
        mt5.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
