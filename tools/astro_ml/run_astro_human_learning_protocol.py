#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, save_json, stable_run_id

THIS = Path(__file__).resolve().parent


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_cmd(args: List[str]) -> str:
    print("\n>>> " + " ".join(str(a) for a in args))
    p = subprocess.run(args, text=True, capture_output=True)
    if p.stdout:
        print(p.stdout)
    if p.stderr:
        print(p.stderr, file=sys.stderr)
    if p.returncode != 0:
        raise SystemExit(p.returncode)
    return p.stdout or ""


def grab(stdout: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}=(.+)$", stdout, flags=re.MULTILINE)
    return m.group(1).strip() if m else ""


def common_rel(path: str, common: Path) -> str:
    p = Path(path)
    try:
        return str(p.relative_to(common))
    except Exception:
        return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Human-like Astro Learning Protocol: auto fetch MT5 rates, resolve/build astro features, train, and build skeptical cognitive memory.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--symbol", default="", help="MT5 symbol. Default = asset.")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--from", dest="from_dt", required=True)
    ap.add_argument("--to", dest="to_dt", required=True)
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--astro-csv", default="", help="Optional existing astro CSV. If absent, archive is searched or built.")
    ap.add_argument("--price-csv", default="", help="Optional existing price CSV. If absent, MT5 is fetched.")
    ap.add_argument("--skip-mt5-fetch", action="store_true")
    ap.add_argument("--force-build-astro", action="store_true")
    ap.add_argument("--broker-gmt-offset-hours", type=float, default=3.0)
    ap.add_argument("--terminal-path", default="")
    ap.add_argument("--preset", choices=["sanity", "direction_only", "professional"], default="professional")
    ap.add_argument("--horizons", default="30,60,120")
    ap.add_argument("--run-walk-forward", action="store_true")
    ap.add_argument("--train-days", type=int, default=120)
    ap.add_argument("--test-days", type=int, default=20)
    ap.add_argument("--step-days", type=int, default=20)
    ap.add_argument("--embargo-bars", type=int, default=120)
    ap.add_argument("--cognitive-min-support", type=int, default=80)
    ap.add_argument("--cognitive-min-lift", type=float, default=1.10)
    ap.add_argument("--cognitive-max-gap", type=float, default=0.18)
    args = ap.parse_args()

    common = Path(args.common_files)
    asset = args.asset.upper()
    symbol = args.symbol or asset
    protocol_id = f"{now_id()}_{stable_run_id([asset, args.timeframe, args.from_dt, args.to_dt, args.preset, 'human_learning'])}"
    out_root = common / "astro_ml" / "human_learning_protocols" / asset / args.timeframe / protocol_id
    ensure_dir(out_root)

    manifest: Dict[str, object] = {
        "protocol_id": protocol_id,
        "asset": asset,
        "symbol": symbol,
        "timeframe": args.timeframe,
        "from": args.from_dt,
        "to": args.to_dt,
        "preset": args.preset,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "out_root": str(out_root),
        "steps": [],
    }

    # 1) Price CSV from MT5 unless supplied.
    price_csv = args.price_csv
    if not price_csv and not args.skip_mt5_fetch:
        safe_from = args.from_dt[:10].replace("-", "").replace(".", "")
        safe_to = args.to_dt[:10].replace("-", "").replace(".", "")
        out_name = f"astro_ml_prices_{symbol}_{args.timeframe}_{safe_from}_to_{safe_to}.csv"
        cmd = [sys.executable, str(THIS / "fetch_mt5_rates.py"), "--symbol", symbol, "--timeframe", args.timeframe, "--from", args.from_dt, "--to", args.to_dt, "--common-files", str(common), "--out-csv", out_name]
        if args.terminal_path:
            cmd += ["--terminal-path", args.terminal_path]
        stdout = run_cmd(cmd)
        price_csv = common_rel(grab(stdout, "MT5_RATES_CSV"), common)
        manifest["steps"].append({"step": "fetch_mt5_rates", "price_csv": price_csv})
    elif not price_csv:
        raise SystemExit("price_csv is empty and --skip-mt5-fetch was used. Provide --price-csv.")
    else:
        manifest["steps"].append({"step": "use_existing_price_csv", "price_csv": price_csv})

    # 2) Astro CSV from archive or deterministic builder.
    astro_csv = args.astro_csv
    if not astro_csv or args.force_build_astro:
        cmd = [
            sys.executable, str(THIS / "resolve_astro_feature_store.py"),
            "--asset", asset,
            "--timeframe", args.timeframe,
            "--from", args.from_dt,
            "--to", args.to_dt,
            "--common-files", str(common),
            "--broker-gmt-offset-hours", str(args.broker_gmt_offset_hours),
        ]
        if astro_csv:
            cmd += ["--preferred-csv", astro_csv]
        if args.force_build_astro:
            cmd += ["--force-build"]
        stdout = run_cmd(cmd)
        astro_csv = common_rel(grab(stdout, "ASTRO_FEATURE_CSV"), common)
        manifest["steps"].append({"step": "resolve_or_build_astro", "astro_csv": astro_csv, "source": grab(stdout, "ASTRO_FEATURE_SOURCE")})
    else:
        manifest["steps"].append({"step": "use_existing_astro_csv", "astro_csv": astro_csv})

    # 3) Run classic professional protocol.
    proto_cmd = [
        sys.executable, str(THIS / "run_astro_ml_protocol.py"),
        "--astro-csv", astro_csv,
        "--price-csv", price_csv,
        "--asset", asset,
        "--timeframe", args.timeframe,
        "--common-files", str(common),
        "--preset", args.preset,
        "--horizons", args.horizons,
    ]
    if args.run_walk_forward:
        proto_cmd += ["--run-walk-forward", "--train-days", str(args.train_days), "--test-days", str(args.test_days), "--step-days", str(args.step_days), "--embargo-bars", str(args.embargo_bars)]
    proto_stdout = run_cmd(proto_cmd)
    proto_dir = grab(proto_stdout, "ASTRO_ML_PROTOCOL_DIR")
    proto_manifest = Path(proto_dir) / "protocol_manifest.json" if proto_dir else None
    dataset_csv = ""
    if proto_manifest and proto_manifest.exists():
        with proto_manifest.open("r", encoding="utf-8") as f:
            pm = json.load(f)
            dataset_csv = pm.get("dataset_csv", "")
    manifest["steps"].append({"step": "classic_protocol", "protocol_dir": proto_dir, "dataset_csv": dataset_csv})

    # 4) Build cognitive/human-like memory.
    if dataset_csv:
        cog_cmd = [
            sys.executable, str(THIS / "build_cognitive_astro_memory.py"),
            "--dataset-csv", dataset_csv,
            "--asset", asset,
            "--timeframe", args.timeframe,
            "--common-files", str(common),
            "--min-support", str(args.cognitive_min_support),
            "--min-lift", str(args.cognitive_min_lift),
            "--max-stability-gap", str(args.cognitive_max_gap),
        ]
        cog_stdout = run_cmd(cog_cmd)
        cog_dir = grab(cog_stdout, "COGNITIVE_MEMORY_DIR")
        manifest["steps"].append({"step": "cognitive_memory", "cognitive_memory_dir": cog_dir, "accepted_rules": grab(cog_stdout, "ACCEPTED_RULES")})
    else:
        manifest["steps"].append({"step": "cognitive_memory", "status": "skipped_no_dataset"})

    save_json(out_root / "human_learning_manifest.json", manifest)
    md = [f"# Astro Human Learning Protocol - {asset} {args.timeframe}\n"]
    md.append("This run fetched/used prices, resolved/built astro features, trained interpretable models, and built skeptical cognitive memory.\n")
    for s in manifest["steps"]:  # type: ignore[index]
        md.append(f"- `{s.get('step')}`: `{s}`")
    (out_root / "HUMAN_LEARNING_REPORT.md").write_text("\n".join(md), encoding="utf-8")

    print(f"HUMAN_LEARNING_PROTOCOL_ID={protocol_id}")
    print(f"HUMAN_LEARNING_PROTOCOL_DIR={out_root}")
    print(f"HUMAN_LEARNING_REPORT={out_root / 'HUMAN_LEARNING_REPORT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
