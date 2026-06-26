#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, find_col, normalize_time_column, read_csv_flexible

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BUILDER = PROJECT_ROOT / "tools" / "astro_feature_builder" / "astro_feature_builder.py"

TF_MINUTES = {
    "M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M6": 6, "M10": 10, "M12": 12, "M15": 15, "M20": 20, "M30": 30,
    "H1": 60, "H2": 120, "H3": 180, "H4": 240, "H6": 360, "H8": 480, "H12": 720, "D1": 1440,
}

ASSET_NATAL_DEFAULTS = {
    "NAS100": {
        "label": "nasdaq100_index_1985_ny_open",
        "local_datetime": "1985-01-31 09:30:00",
        "utc_offset": -5.0,
        "lat": 40.7128,
        "lon": -74.0060,
    },
    "US100": {
        "label": "nasdaq100_index_1985_ny_open",
        "local_datetime": "1985-01-31 09:30:00",
        "utc_offset": -5.0,
        "lat": 40.7128,
        "lon": -74.0060,
    },
    "GOLD": {
        "label": "gold_comex_1974_ny_open",
        "local_datetime": "1974-12-31 08:20:00",
        "utc_offset": -5.0,
        "lat": 40.7128,
        "lon": -74.0060,
    },
    "XAUUSD": {
        "label": "gold_comex_1974_ny_open",
        "local_datetime": "1974-12-31 08:20:00",
        "utc_offset": -5.0,
        "lat": 40.7128,
        "lon": -74.0060,
    },
}


def parse_dt(s: str) -> datetime:
    s = s.strip().replace(".", "-").replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse datetime: {s}")


def schema_rank(schema_version: str) -> int:
    text = str(schema_version).strip().lower()
    if "_v" in text:
        try:
            return int(text.rsplit("_v", 1)[1])
        except Exception:
            return 0
    return 0


def covers(path: Path, start: datetime, end: datetime, min_schema_rank: int = 4) -> Tuple[bool, str]:
    try:
        df = read_csv_flexible(path)
        if df.empty:
            return False, "empty"
        df, tc = normalize_time_column(df)
        schema_text = ""
        if "schema_version" in df.columns and len(df) > 0:
            schema_text = str(df["schema_version"].iloc[0])
            rank = schema_rank(schema_text)
            if rank < min_schema_rank:
               return False, f"schema_too_old={schema_text}"
        first = pd.to_datetime(df[tc].iloc[0]).to_pydatetime()
        last = pd.to_datetime(df[tc].iloc[-1]).to_pydatetime()
        ok = first <= start and last >= end
        return ok, f"first={first} last={last} rows={len(df)} schema={schema_text}"
    except Exception as exc:
        return False, f"read_error={exc}"


def find_archive(common: Path, asset: str, timeframe: str, start: datetime, end: datetime, preferred: str = "", min_schema_rank: int = 4) -> Optional[Path]:
    candidates = []
    if preferred:
        p = Path(preferred)
        if not p.is_absolute():
            p = common / p
        if p.exists():
            candidates.append(p)
    roots = [
        common,
        common / "astro_archive" / asset / timeframe,
        common / "astro" / "archive" / asset / timeframe,
        common / "astro" / "features" / asset / timeframe,
    ]
    terms = [asset.lower(), timeframe.lower(), "astro"]
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.csv"):
            name = p.name.lower()
            if all(t in name for t in terms[:2]) or ("astro" in name and asset.lower() in name):
                candidates.append(p)
    seen = set()
    unique = []
    for p in candidates:
        if str(p).lower() not in seen:
            unique.append(p); seen.add(str(p).lower())
    for p in sorted(unique, key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True):
        ok, msg = covers(p, start, end, min_schema_rank=min_schema_rank)
        if ok:
            print(f"ASTRO_ARCHIVE_HIT={p}")
            print(f"ASTRO_ARCHIVE_INFO={msg}")
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolve an existing astro feature store from archive or build it deterministically.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--from", dest="from_dt", required=True, help="Broker time start, e.g. 2026-06-22 00:00")
    ap.add_argument("--to", dest="to_dt", required=True, help="Broker time end, exclusive-ish, e.g. 2026-06-27 23:59")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--preferred-csv", default="")
    ap.add_argument("--force-build", action="store_true")
    ap.add_argument("--broker-gmt-offset-hours", type=float, default=3.0)
    ap.add_argument("--out-csv", default="")
    ap.add_argument("--ephe-path", default="")
    ap.add_argument("--natal-label", default="")
    ap.add_argument("--natal-local-datetime", default="")
    ap.add_argument("--natal-utc-offset-hours", type=float, default=None)
    ap.add_argument("--natal-lat", type=float, default=None)
    ap.add_argument("--natal-lon", type=float, default=None)
    ap.add_argument("--house-lat", type=float, default=None)
    ap.add_argument("--house-lon", type=float, default=None)
    ap.add_argument("--min-schema-rank", type=int, default=4, help="Minimum acceptable astro schema rank when reusing archives.")
    args = ap.parse_args()

    common = Path(args.common_files)
    asset = args.asset.upper()
    timeframe = args.timeframe.upper()
    if timeframe not in TF_MINUTES:
        raise SystemExit(f"Unsupported timeframe for astro builder: {timeframe}")
    start = parse_dt(args.from_dt)
    end = parse_dt(args.to_dt)

    if not args.force_build:
        hit = find_archive(common, asset, timeframe, start, end, args.preferred_csv, min_schema_rank=args.min_schema_rank)
        if hit is not None:
            print(f"ASTRO_FEATURE_CSV={hit}")
            print("ASTRO_FEATURE_SOURCE=archive")
            return 0

    defaults = ASSET_NATAL_DEFAULTS.get(asset, ASSET_NATAL_DEFAULTS.get("NAS100", {}))
    natal_label = args.natal_label or defaults.get("label", f"{asset.lower()}_natal")
    natal_dt = args.natal_local_datetime or defaults.get("local_datetime", "1985-01-31 09:30:00")
    natal_off = args.natal_utc_offset_hours if args.natal_utc_offset_hours is not None else defaults.get("utc_offset", -5.0)
    natal_lat = args.natal_lat if args.natal_lat is not None else defaults.get("lat", 40.7128)
    natal_lon = args.natal_lon if args.natal_lon is not None else defaults.get("lon", -74.0060)

    if args.out_csv:
        out_csv = Path(args.out_csv)
        if not out_csv.is_absolute():
            out_csv = common / out_csv
    else:
        safe_from = start.strftime("%Y%m%d")
        safe_to = end.strftime("%Y%m%d")
        out_csv = common / "astro_archive" / asset / timeframe / f"astro_{asset}_{timeframe}_{safe_from}_to_{safe_to}_{natal_label}_mql.csv"
    ensure_dir(out_csv.parent)

    cmd = [
        sys.executable, str(BUILDER),
        "--start-broker", start.strftime("%Y-%m-%d %H:%M:%S"),
        "--end-broker", end.strftime("%Y-%m-%d %H:%M:%S"),
        "--timeframe-minutes", str(TF_MINUTES[timeframe]),
        "--broker-gmt-offset-hours", str(args.broker_gmt_offset_hours),
        "--out-csv", str(out_csv),
        "--natal-local-datetime", str(natal_dt),
        "--natal-utc-offset-hours", str(natal_off),
        "--natal-lat", str(natal_lat),
        "--natal-lon", str(natal_lon),
        "--natal-label", natal_label,
    ]
    if args.house_lat is not None and args.house_lon is not None:
        cmd += ["--house-lat", str(args.house_lat), "--house-lon", str(args.house_lon)]
    if args.ephe_path:
        cmd += ["--ephe-path", args.ephe_path]

    print(">>> " + " ".join(cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)

    print(f"ASTRO_FEATURE_CSV={out_csv}")
    print("ASTRO_FEATURE_SOURCE=built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
