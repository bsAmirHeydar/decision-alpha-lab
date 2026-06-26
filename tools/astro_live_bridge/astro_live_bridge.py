#!/usr/bin/env python3
"""
Decision Alpha Lab - EXP0013 Astro Live Bridge V2

Python computes rolling astro rows and writes them atomically into
MetaQuotes Common\\Files for the MQL5 dashboard EA.

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
    house_lat: float | None = None,
    house_lon: float | None = None,
    house_system: str = "P",
    natal_local_datetime: str = "",
    natal_utc_offset_hours: float = 0.0,
    natal_lat: float | None = None,
    natal_lon: float | None = None,
    natal_house_system: str = "P",
    natal_label: str = "",
    doctrine_id: str = "astro_only_doctrine_v1",
    schema_version: str = "astro_feature_schema_v4",
    zodiac_mode: str = "tropical",
    body_universe: str = "major7_outer_nodes",
    orb_family: str = "major_ptolemaic_6deg",
    parallel_orb_limit: float = 1.0,
    config_path: str = "",
) -> None:
    cmd = [
        sys.executable,
        str(builder),
    ]
    if config_path:
        cmd += ["--config", config_path]
    cmd += [
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
        "--doctrine-id",
        doctrine_id,
        "--schema-version",
        schema_version,
        "--zodiac-mode",
        zodiac_mode,
        "--body-universe",
        body_universe,
        "--orb-family",
        orb_family,
        "--parallel-orb-limit",
        str(parallel_orb_limit),
    ]
    if house_lat is not None or house_lon is not None:
        if house_lat is None or house_lon is None:
            raise ValueError("Provide both --house-lat and --house-lon for live houses")
        cmd += ["--house-lat", str(house_lat), "--house-lon", str(house_lon), "--house-system", str(house_system)]
    if natal_local_datetime:
        cmd += ["--natal-local-datetime", natal_local_datetime, "--natal-utc-offset-hours", str(natal_utc_offset_hours)]
        if natal_lat is not None or natal_lon is not None:
            if natal_lat is None or natal_lon is None:
                raise ValueError("Provide both --natal-lat and --natal-lon for natal houses")
            cmd += ["--natal-lat", str(natal_lat), "--natal-lon", str(natal_lon), "--natal-house-system", str(natal_house_system)]
        if natal_label:
            cmd += ["--natal-label", natal_label]
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
            house_lat=args.house_lat,
            house_lon=args.house_lon,
            house_system=args.house_system,
            natal_local_datetime=args.natal_local_datetime,
            natal_utc_offset_hours=args.natal_utc_offset_hours,
            natal_lat=args.natal_lat,
            natal_lon=args.natal_lon,
            natal_house_system=args.natal_house_system,
            natal_label=args.natal_label,
            doctrine_id=args.doctrine_id,
            schema_version=args.schema_version,
            zodiac_mode=args.zodiac_mode,
            body_universe=args.body_universe,
            orb_family=args.orb_family,
            parallel_orb_limit=args.parallel_orb_limit,
            config_path=args.config,
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
    ap.add_argument("--config", default="", help="Optional builder doctrine JSON config")
    ap.add_argument("--builder", default="tools/astro_feature_builder/astro_feature_builder.py")
    ap.add_argument("--ephe-path", default="tools/astro_feature_builder/ephe")
    ap.add_argument("--common-files", required=True, help="MetaQuotes Common\\Files path")
    ap.add_argument("--output-name", default="astro_live_mql.csv")
    ap.add_argument("--status-name", default="astro_live_status.json")
    ap.add_argument("--broker-gmt-offset-hours", type=float, default=3.0)
    ap.add_argument("--timeframe-minutes", type=int, default=1)
    ap.add_argument("--history-hours", type=int, default=48)
    ap.add_argument("--future-hours", type=int, default=6)
    ap.add_argument("--house-lat", type=float, default=None, help="Optional latitude for live house cusps")
    ap.add_argument("--house-lon", type=float, default=None, help="Optional longitude for live house cusps")
    ap.add_argument("--house-system", default="P", help="House system code passed to Swiss Ephemeris, default P=Placidus")
    ap.add_argument("--natal-local-datetime", default="", help="Optional natal/inception local datetime")
    ap.add_argument("--natal-utc-offset-hours", type=float, default=0.0, help="UTC offset used for natal local datetime")
    ap.add_argument("--natal-lat", type=float, default=None, help="Optional natal latitude")
    ap.add_argument("--natal-lon", type=float, default=None, help="Optional natal longitude")
    ap.add_argument("--natal-house-system", default="P", help="Natal house system code")
    ap.add_argument("--natal-label", default="", help="Optional natal chart label")
    ap.add_argument("--doctrine-id", default="astro_only_doctrine_v1")
    ap.add_argument("--schema-version", default="astro_feature_schema_v4")
    ap.add_argument("--zodiac-mode", default="tropical")
    ap.add_argument("--body-universe", default="major7_outer_nodes")
    ap.add_argument("--orb-family", default="major_ptolemaic_6deg")
    ap.add_argument("--parallel-orb-limit", type=float, default=1.0)
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
