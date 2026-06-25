#!/usr/bin/env python3
"""
Decision Alpha Lab - EXP0013 Astro Live Bridge

Purpose
-------
This is the recommended live architecture:
Python computes or exports the astro state.
MetaTrader reads a small rolling CSV from Common\\Files and renders it.

This avoids:
- custom-indicator loading problems in Strategy Tester
- huge full-year CSV reloads in live mode
- MQL5 trying to calculate ephemeris directly
- WebRequest permission problems

This script is intentionally simple. The existing astro_feature_builder remains the
authoritative generator for full historical datasets. For production, wire the same
feature-building functions into this loop and write a rolling CSV with the same schema
as the historical MQL CSV.

Usage model
-----------
1. Run Python continuously.
2. Every N seconds, build/rebuild a small rolling CSV, for example last 2 days + next 6 hours.
3. Write it atomically into:
   C:\\Users\\<USER>\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\astro_live_mql.csv
4. In MT5 EA:
   InpAstroCsvFile = astro_live_mql.csv
   InpReloadCsvEverySeconds = 10 or 30
   InpBrokerGmtOffsetHours = 0
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path


def atomic_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False, dir=str(dst.parent), suffix=".tmp") as f:
        tmp = Path(f.name)
    try:
        shutil.copyfile(src, tmp)
        os.replace(tmp, dst)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def broker_now(offset_hours: float) -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=offset_hours)


def run_builder(
    builder: Path,
    out_csv: Path,
    start_broker: datetime,
    end_broker: datetime,
    timeframe_minutes: int,
    broker_gmt_offset_hours: float,
    ephe_path: Path,
) -> None:
    cmd = [
        sys.executable,
        str(builder),
        "--start-broker",
        start_broker.strftime("%Y-%m-%d %H:%M:%S"),
        "--end-broker",
        end_broker.strftime("%Y-%m-%d %H:%M:%S"),
        "--timeframe-minutes",
        str(timeframe_minutes),
        "--broker-gmt-offset-hours",
        str(broker_gmt_offset_hours),
        "--ephe-path",
        str(ephe_path),
        "--out-csv",
        str(out_csv),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--builder", default="tools/astro_feature_builder/astro_feature_builder.py")
    ap.add_argument("--ephe-path", default="tools/astro_feature_builder/ephe")
    ap.add_argument("--common-files", required=True, help="MetaQuotes Common\\Files path")
    ap.add_argument("--output-name", default="astro_live_mql.csv")
    ap.add_argument("--broker-gmt-offset-hours", type=float, default=3.0)
    ap.add_argument("--timeframe-minutes", type=int, default=1)
    ap.add_argument("--history-hours", type=int, default=48)
    ap.add_argument("--future-hours", type=int, default=6)
    ap.add_argument("--refresh-seconds", type=int, default=60)
    args = ap.parse_args()

    builder = Path(args.builder)
    ephe_path = Path(args.ephe_path)
    common_out = Path(args.common_files) / args.output_name
    work_dir = Path("lab/03_experiments/EXP0013_astro_feature_store/live_runtime")
    work_dir.mkdir(parents=True, exist_ok=True)

    print("EXP0013 Astro Live Bridge")
    print("Common output:", common_out)
    print("Refresh seconds:", args.refresh_seconds)

    while True:
        now_broker = broker_now(args.broker_gmt_offset_hours)
        start_broker = now_broker - timedelta(hours=args.history_hours)
        end_broker = now_broker + timedelta(hours=args.future_hours)

        local_csv = work_dir / args.output_name
        try:
            run_builder(
                builder=builder,
                out_csv=local_csv,
                start_broker=start_broker,
                end_broker=end_broker,
                timeframe_minutes=args.timeframe_minutes,
                broker_gmt_offset_hours=args.broker_gmt_offset_hours,
                ephe_path=ephe_path,
            )
            atomic_copy(local_csv, common_out)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "updated", common_out)
        except Exception as exc:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ERROR", repr(exc), file=sys.stderr)

        time.sleep(max(5, args.refresh_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
