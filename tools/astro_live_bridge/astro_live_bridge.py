#!/usr/bin/env python3
"""
Decision Alpha Lab - EXP0013 Astro Live Bridge V2

Python computes rolling astro rows and writes them atomically into
MetaQuotes Common\Files for the MQL5 dashboard EA.

The bridge deliberately uses files instead of WebRequest or sockets:
- stable in live MT5
- easy to inspect
- no MT5 permissions required except normal Files/Common Files access
- safe atomic replacement so MQL never reads a half-written CSV

The CSV time contract is unchanged:
- Python writes broker_time already aligned to broker time
- Python writes utc_time as the astronomical UTC time
- MQL matches chart candle open directly to CSV broker_time
- MQL does not apply a second GMT shift
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def broker_now(offset_hours: float) -> datetime:
    return utc_now() + timedelta(hours=offset_hours)


def atomic_write_text(dst: Path, text: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(dst.parent), suffix=".tmp", encoding="utf-8") as f:
        tmp = Path(f.name)
        f.write(text)
    try:
        os.replace(tmp, dst)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


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


def write_status(
    status_path: Path,
    *,
    ok: bool,
    output_csv: Path,
    start_broker: datetime,
    end_broker: datetime,
    refresh_seconds: int,
    rows_hint: int | None = None,
    error: str | None = None,
) -> None:
    payload = {
        "ok": ok,
        "updated_utc": utc_now().strftime("%Y-%m-%d %H:%M:%S"),
        "output_csv": str(output_csv),
        "broker_start": start_broker.strftime("%Y-%m-%d %H:%M:%S"),
        "broker_end": end_broker.strftime("%Y-%m-%d %H:%M:%S"),
        "refresh_seconds": refresh_seconds,
        "rows_hint": rows_hint,
        "error": error or "",
    }
    atomic_write_text(status_path, json.dumps(payload, ensure_ascii=False, indent=2))


def count_csv_rows(path: Path) -> int | None:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            n = sum(1 for _ in f)
        return max(0, n - 1)
    except OSError:
        return None


def build_once(args: argparse.Namespace, work_dir: Path, common_out: Path, status_out: Path) -> bool:
    now_broker = broker_now(args.broker_gmt_offset_hours)
    start_broker = now_broker - timedelta(hours=args.history_hours)
    end_broker = now_broker + timedelta(hours=args.future_hours)
    local_csv = work_dir / args.output_name

    try:
        run_builder(
            builder=Path(args.builder),
            out_csv=local_csv,
            start_broker=start_broker,
            end_broker=end_broker,
            timeframe_minutes=args.timeframe_minutes,
            broker_gmt_offset_hours=args.broker_gmt_offset_hours,
            ephe_path=Path(args.ephe_path),
        )
        rows = count_csv_rows(local_csv)
        atomic_copy(local_csv, common_out)
        write_status(
            status_out,
            ok=True,
            output_csv=common_out,
            start_broker=start_broker,
            end_broker=end_broker,
            refresh_seconds=args.refresh_seconds,
            rows_hint=rows,
        )
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "updated", common_out, "rows", rows)
        return True
    except Exception as exc:
        write_status(
            status_out,
            ok=False,
            output_csv=common_out,
            start_broker=start_broker,
            end_broker=end_broker,
            refresh_seconds=args.refresh_seconds,
            error=repr(exc),
        )
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ERROR", repr(exc), file=sys.stderr)
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--builder", default="tools/astro_feature_builder/astro_feature_builder.py")
    ap.add_argument("--ephe-path", default="tools/astro_feature_builder/ephe")
    ap.add_argument("--common-files", required=True, help="MetaQuotes Common\\Files path")
    ap.add_argument("--output-name", default="astro_live_mql.csv")
    ap.add_argument("--status-name", default="astro_live_status.json")
    ap.add_argument("--broker-gmt-offset-hours", type=float, default=3.0)
    ap.add_argument("--timeframe-minutes", type=int, default=1)
    ap.add_argument("--history-hours", type=int, default=48)
    ap.add_argument("--future-hours", type=int, default=6)
    ap.add_argument("--refresh-seconds", type=int, default=60)
    ap.add_argument("--once", action="store_true", help="Build once and exit")
    args = ap.parse_args()

    common_dir = Path(args.common_files)
    common_out = common_dir / args.output_name
    status_out = common_dir / args.status_name
    work_dir = Path("lab/03_experiments/EXP0013_astro_feature_store/live_runtime")
    work_dir.mkdir(parents=True, exist_ok=True)

    print("EXP0013 Astro Live Bridge V2")
    print("Common CSV:   ", common_out)
    print("Status JSON:  ", status_out)
    print("Refresh sec:  ", args.refresh_seconds)

    if args.once:
        return 0 if build_once(args, work_dir, common_out, status_out) else 1

    while True:
        build_once(args, work_dir, common_out, status_out)
        time.sleep(max(5, args.refresh_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
