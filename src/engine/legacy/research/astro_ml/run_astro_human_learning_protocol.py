#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, normalize_time_column, read_csv_flexible, save_json, stable_run_id

THIS = Path(__file__).resolve().parent


TF_MINUTES = {
    "M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M6": 6, "M10": 10, "M12": 12, "M15": 15, "M20": 20, "M30": 30,
    "H1": 60, "H2": 120, "H3": 180, "H4": 240, "H6": 360, "H8": 480, "H12": 720, "D1": 1440,
}


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_dt(s: str) -> datetime:
    s = s.strip().replace(".", "-").replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse datetime: {s}")


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


def resolve_common_path(path: str, common: Path) -> Path:
    p = Path(path)
    if not p.is_absolute():
        p = common / p
    return p


def file_time_range(path: Path) -> Tuple[bool, str, Optional[datetime], Optional[datetime], int]:
    try:
        if not path.exists():
            return False, "missing", None, None, 0
        df = read_csv_flexible(path)
        if df.empty:
            return False, "empty", None, None, 0
        df, tc = normalize_time_column(df)
        if df.empty:
            return False, "no_valid_time", None, None, 0
        first = pd.to_datetime(df[tc].iloc[0]).to_pydatetime()
        last = pd.to_datetime(df[tc].iloc[-1]).to_pydatetime()
        return True, f"first={first} last={last} rows={len(df)}", first, last, len(df)
    except Exception as exc:
        return False, f"read_error={exc}", None, None, 0


def covers_strict(path: Path, start: datetime, end: datetime, min_rows: int = 10) -> Tuple[bool, str]:
    ok, msg, first, last, rows = file_time_range(path)
    if not ok:
        return False, msg
    assert first is not None and last is not None
    cover = first <= start and last >= end and rows >= min_rows
    return cover, msg


def overlaps_usefully(path: Path, start: datetime, end: datetime, min_rows: int = 10) -> Tuple[bool, str]:
    """Looser than full coverage; suitable for market prices over weekends/closed sessions."""
    ok, msg, first, last, rows = file_time_range(path)
    if not ok:
        return False, msg
    assert first is not None and last is not None
    overlap = last >= start and first <= end and rows >= min_rows
    return overlap, msg


def find_price_archive(common: Path, symbol: str, timeframe: str, start: datetime, end: datetime, preferred: str = "", strict: bool = False) -> Tuple[Optional[Path], str]:
    candidates: List[Path] = []
    if preferred:
        p = resolve_common_path(preferred, common)
        if p.exists():
            candidates.append(p)
        else:
            return None, f"preferred_missing={p}"

    roots = [
        common,
        common / "astro_ml" / "prices" / symbol.upper() / timeframe.upper(),
        common / "astro_ml" / "prices",
        common / "prices" / symbol.upper() / timeframe.upper(),
    ]
    if not preferred:
        symbol_l = symbol.lower()
        tf_l = timeframe.lower()
        for root in roots:
            if not root.exists():
                continue
            for p in root.rglob("*.csv"):
                name = p.name.lower()
                if symbol_l in name and tf_l in name and ("price" in name or "rates" in name or "ohlc" in name or "astro_ml_prices" in name):
                    candidates.append(p)

    seen = set()
    unique: List[Path] = []
    for c in candidates:
        k = str(c).lower()
        if k not in seen:
            seen.add(k); unique.append(c)

    check = covers_strict if strict else overlaps_usefully
    rejected: List[str] = []
    for p in sorted(unique, key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True):
        good, msg = check(p, start, end)
        if good:
            return p, msg
        rejected.append(f"{p.name}: {msg}")
    return None, "; ".join(rejected[:8]) if rejected else "no_candidates"


def fetch_price_from_mt5(common: Path, symbol: str, timeframe: str, from_dt: str, to_dt: str, terminal_path: str = "") -> str:
    start = parse_dt(from_dt)
    end = parse_dt(to_dt)
    safe_from = start.strftime("%Y%m%d")
    safe_to = end.strftime("%Y%m%d")
    out_name = str(Path("astro_ml") / "prices" / symbol.upper() / timeframe.upper() / f"astro_ml_prices_{symbol}_{timeframe}_{safe_from}_to_{safe_to}.csv")
    cmd = [
        sys.executable, str(THIS / "fetch_mt5_rates.py"),
        "--symbol", symbol,
        "--timeframe", timeframe,
        "--from", from_dt,
        "--to", to_dt,
        "--common-files", str(common),
        "--out-csv", out_name,
    ]
    if terminal_path:
        cmd += ["--terminal-path", terminal_path]
    stdout = run_cmd(cmd)
    return common_rel(grab(stdout, "MT5_RATES_CSV"), common)


def resolve_or_fetch_price(common: Path, symbol: str, timeframe: str, from_dt: str, to_dt: str, preferred: str, skip_fetch: bool, force_fetch: bool, terminal_path: str, strict_coverage: bool) -> Tuple[str, Dict[str, str]]:
    start = parse_dt(from_dt)
    end = parse_dt(to_dt)
    if not force_fetch:
        hit, info = find_price_archive(common, symbol, timeframe, start, end, preferred=preferred, strict=strict_coverage)
        if hit is not None:
            return common_rel(str(hit), common), {"source": "price_archive", "path": str(hit), "info": info}
        if preferred and skip_fetch:
            raise SystemExit(f"Preferred price CSV was not usable and MT5 fetch is disabled: {info}")
        if preferred:
            print(f"PRICE_CSV_NOT_USABLE={info}")
    if skip_fetch:
        raise SystemExit("No usable price CSV found and --skip-mt5-fetch was used. Remove --skip-mt5-fetch or provide a usable --price-csv.")
    fetched = fetch_price_from_mt5(common, symbol, timeframe, from_dt, to_dt, terminal_path)
    return fetched, {"source": "mt5_fetched", "path": fetched}


def resolve_or_build_astro(common: Path, asset: str, timeframe: str, from_dt: str, to_dt: str, preferred: str, force_build: bool, broker_gmt_offset_hours: float, natal_args: Dict[str, str]) -> Tuple[str, Dict[str, str]]:
    cmd = [
        sys.executable, str(THIS / "resolve_astro_feature_store.py"),
        "--asset", asset,
        "--timeframe", timeframe,
        "--from", from_dt,
        "--to", to_dt,
        "--common-files", str(common),
        "--broker-gmt-offset-hours", str(broker_gmt_offset_hours),
    ]
    if preferred:
        cmd += ["--preferred-csv", preferred]
    if force_build:
        cmd += ["--force-build"]
    for k, v in natal_args.items():
        if v not in (None, ""):
            cmd += [k, str(v)]
    stdout = run_cmd(cmd)
    astro = common_rel(grab(stdout, "ASTRO_FEATURE_CSV"), common)
    source = grab(stdout, "ASTRO_FEATURE_SOURCE") or "unknown"
    return astro, {"source": source, "path": astro}


def main() -> int:
    ap = argparse.ArgumentParser(description="Self-healing Human-like Astro Learning Protocol. Give symbol/date only; it resolves or fetches price data and resolves or builds astro features automatically.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--symbol", default="", help="MT5 symbol. Default = asset.")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--from", dest="from_dt", required=True)
    ap.add_argument("--to", dest="to_dt", required=True)
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--astro-csv", default="", help="Optional existing astro CSV. If missing/not covering range, archive is searched or built.")
    ap.add_argument("--price-csv", default="", help="Optional existing price CSV. If missing/not usable, archive is searched or MT5 is fetched.")
    ap.add_argument("--skip-mt5-fetch", action="store_true", help="Disable MT5 fetching; fail if no usable price CSV exists.")
    ap.add_argument("--force-fetch-price", action="store_true", help="Ignore existing price CSV/archive and fetch from MT5.")
    ap.add_argument("--strict-price-coverage", action="store_true", help="Require price CSV to cover the entire date range. Default only requires useful overlap to handle market-close/weekends.")
    ap.add_argument("--force-build-astro", action="store_true", help="Ignore existing astro CSV/archive and rebuild from project astro_feature_builder.")
    ap.add_argument("--broker-gmt-offset-hours", type=float, default=3.0)
    ap.add_argument("--terminal-path", default="")
    ap.add_argument("--natal-label", default="")
    ap.add_argument("--natal-local-datetime", default="")
    ap.add_argument("--natal-utc-offset-hours", default="")
    ap.add_argument("--natal-lat", default="")
    ap.add_argument("--natal-lon", default="")
    ap.add_argument("--house-lat", default="")
    ap.add_argument("--house-lon", default="")
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
    ap.add_argument("--skip-antifragile", action="store_true", help="Skip the principle-first antifragile learning layer.")
    ap.add_argument("--antifragile-targets", default="", help="Comma-separated label targets for antifragile learning. Default = core targets found in dataset.")
    ap.add_argument("--antifragile-min-rule-support", type=int, default=120)
    ap.add_argument("--antifragile-min-oos-support", type=int, default=40)
    ap.add_argument("--antifragile-min-lift", type=float, default=1.08)
    ap.add_argument("--antifragile-max-gap", type=float, default=0.14)
    ap.add_argument("--enable-neural-challenger", action="store_true", help="Allow a small neural net as a challenger. It is never accepted without OOS survival.")
    ap.add_argument("--neural-min-rows", type=int, default=8000)
    ap.add_argument("--skip-fragility-audit", action="store_true", help="Skip the final antifragile fragility audit/hardening layer.")
    ap.add_argument("--fragility-folds", type=int, default=6)
    ap.add_argument("--fragility-min-fold-support", type=int, default=25)
    ap.add_argument("--fragility-min-survival-rate", type=float, default=0.60)
    ap.add_argument("--fragility-min-median-lift", type=float, default=1.05)
    ap.add_argument("--fragility-min-worst-lift", type=float, default=0.95)
    ap.add_argument("--fragility-max-lift-iqr", type=float, default=0.65)
    ap.add_argument("--fragility-perturb-repeats", type=int, default=24)
    ap.add_argument("--fragility-noise-scale", type=float, default=0.035)
    ap.add_argument("--fragility-dropout-rate", type=float, default=0.10)
    ap.add_argument("--fragility-max-perturb-drop", type=float, default=0.055)
    ap.add_argument("--fragility-max-concept-dependency-drop", type=float, default=0.12)
    ap.add_argument("--fragility-max-rules-per-target", type=int, default=12)
    ap.add_argument("--fragility-max-rules-per-concept-target", type=int, default=4)
    ap.add_argument("--allow-audit-warnings", action="store_true", help="Allow professional protocol to continue even when critical dataset-audit gates fail.")
    ap.add_argument("--audit-min-rows", type=int, default=0, help="Override minimum-row audit gate passed into the core protocol.")
    args = ap.parse_args()

    common = Path(args.common_files)
    asset = args.asset.upper()
    symbol = args.symbol or asset
    timeframe = args.timeframe.upper()
    if timeframe not in TF_MINUTES:
        raise SystemExit(f"Unsupported timeframe: {timeframe}")

    protocol_id = f"{now_id()}_{stable_run_id([asset, timeframe, args.from_dt, args.to_dt, args.preset, 'self_healing_human_learning'])}"
    out_root = common / "astro_ml" / "human_learning_protocols" / asset / timeframe / protocol_id
    ensure_dir(out_root)

    manifest: Dict[str, object] = {
        "protocol_id": protocol_id,
        "asset": asset,
        "symbol": symbol,
        "timeframe": timeframe,
        "from": args.from_dt,
        "to": args.to_dt,
        "preset": args.preset,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "out_root": str(out_root),
        "self_healing_contract": "check price -> reuse archive or fetch MT5; check astro -> reuse archive or build project astro_feature_builder; then build/train/cognitive_memory/antifragile_principles",
        "steps": [],
    }

    # 1) Price CSV: check preferred/archive first, then fetch MT5 if necessary.
    price_csv, price_meta = resolve_or_fetch_price(
        common=common,
        symbol=symbol,
        timeframe=timeframe,
        from_dt=args.from_dt,
        to_dt=args.to_dt,
        preferred=args.price_csv,
        skip_fetch=args.skip_mt5_fetch,
        force_fetch=args.force_fetch_price,
        terminal_path=args.terminal_path,
        strict_coverage=args.strict_price_coverage,
    )
    manifest["steps"].append({"step": "resolve_or_fetch_price", **price_meta, "price_csv": price_csv})

    # 2) Astro CSV: check preferred/archive first, then build from project's astro builder.
    natal_args = {
        "--natal-label": args.natal_label,
        "--natal-local-datetime": args.natal_local_datetime,
        "--natal-utc-offset-hours": args.natal_utc_offset_hours,
        "--natal-lat": args.natal_lat,
        "--natal-lon": args.natal_lon,
        "--house-lat": args.house_lat,
        "--house-lon": args.house_lon,
    }
    astro_csv, astro_meta = resolve_or_build_astro(
        common=common,
        asset=asset,
        timeframe=timeframe,
        from_dt=args.from_dt,
        to_dt=args.to_dt,
        preferred=args.astro_csv,
        force_build=args.force_build_astro,
        broker_gmt_offset_hours=args.broker_gmt_offset_hours,
        natal_args=natal_args,
    )
    manifest["steps"].append({"step": "resolve_or_build_astro", **astro_meta, "astro_csv": astro_csv})

    # 3) Run classic professional protocol.
    proto_cmd = [
        sys.executable, str(THIS / "run_astro_ml_protocol.py"),
        "--astro-csv", astro_csv,
        "--price-csv", price_csv,
        "--asset", asset,
        "--timeframe", timeframe,
        "--common-files", str(common),
        "--preset", args.preset,
        "--horizons", args.horizons,
    ]
    if args.allow_audit_warnings:
        proto_cmd += ["--allow-audit-warnings"]
    if args.audit_min_rows > 0:
        proto_cmd += ["--audit-min-rows", str(args.audit_min_rows)]
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
            "--timeframe", timeframe,
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

    # 5) Antifragile principle-first learning layer.
    # This is deliberately reductive and skeptical: it compresses many mechanical
    # features into broad concepts, tests simple principles before complex models,
    # and rejects patterns that do not survive the chronological OOS segment.
    if dataset_csv and not args.skip_antifragile:
        anti_cmd = [
            sys.executable, str(THIS / "build_antifragile_astro_learning.py"),
            "--dataset-csv", dataset_csv,
            "--asset", asset,
            "--timeframe", timeframe,
            "--common-files", str(common),
            "--min-rule-support", str(args.antifragile_min_rule_support),
            "--min-oos-support", str(args.antifragile_min_oos_support),
            "--min-lift", str(args.antifragile_min_lift),
            "--max-gap", str(args.antifragile_max_gap),
            "--neural-min-rows", str(args.neural_min_rows),
        ]
        if args.antifragile_targets:
            anti_cmd += ["--targets", args.antifragile_targets]
        if args.enable_neural_challenger:
            anti_cmd += ["--enable-neural-challenger"]
        anti_stdout = run_cmd(anti_cmd)
        anti_dir = grab(anti_stdout, "ANTIFRAGILE_MEMORY_DIR")
        manifest["steps"].append({
            "step": "antifragile_learning",
            "antifragile_memory_dir": anti_dir,
            "accepted_principles": grab(anti_stdout, "ANTIFRAGILE_ACCEPTED_PRINCIPLES"),
            "mind": grab(anti_stdout, "ANTIFRAGILE_MIND"),
        })
    else:
        anti_dir = ""
        if args.skip_antifragile:
            manifest["steps"].append({"step": "antifragile_learning", "status": "skipped_by_user"})
        else:
            manifest["steps"].append({"step": "antifragile_learning", "status": "skipped_no_dataset"})

    # 6) Final fragility audit / hardening layer.
    # This audits the learner's thinking: temporal survival, perturbation
    # sensitivity, concept monoculture risk, contradictions, and condition creep.
    if dataset_csv and not args.skip_fragility_audit and not args.skip_antifragile:
        frag_cmd = [
            sys.executable, str(THIS / "build_antifragile_fragility_audit.py"),
            "--dataset-csv", dataset_csv,
            "--asset", asset,
            "--timeframe", timeframe,
            "--common-files", str(common),
            "--folds", str(args.fragility_folds),
            "--min-fold-support", str(args.fragility_min_fold_support),
            "--min-survival-rate", str(args.fragility_min_survival_rate),
            "--min-median-lift", str(args.fragility_min_median_lift),
            "--min-worst-lift", str(args.fragility_min_worst_lift),
            "--max-lift-iqr", str(args.fragility_max_lift_iqr),
            "--perturb-repeats", str(args.fragility_perturb_repeats),
            "--perturb-noise-scale", str(args.fragility_noise_scale),
            "--perturb-dropout-rate", str(args.fragility_dropout_rate),
            "--max-perturb-drop", str(args.fragility_max_perturb_drop),
            "--max-concept-dependency-drop", str(args.fragility_max_concept_dependency_drop),
            "--max-rules-per-target", str(args.fragility_max_rules_per_target),
            "--max-rules-per-concept-target", str(args.fragility_max_rules_per_concept_target),
        ]
        if anti_dir:
            frag_cmd += ["--antifragile-dir", anti_dir]
        if args.antifragile_targets:
            frag_cmd += ["--targets", args.antifragile_targets]
        frag_stdout = run_cmd(frag_cmd)
        manifest["steps"].append({
            "step": "fragility_audit",
            "fragility_audit_dir": grab(frag_stdout, "FRAGILITY_AUDIT_DIR"),
            "decision_memory": grab(frag_stdout, "FRAGILITY_DECISION_MEMORY"),
            "hardened_principles": grab(frag_stdout, "HARDENED_PRINCIPLES"),
            "fragility_flags": grab(frag_stdout, "FRAGILITY_FLAGS"),
        })
    elif args.skip_fragility_audit:
        manifest["steps"].append({"step": "fragility_audit", "status": "skipped_by_user"})
    else:
        manifest["steps"].append({"step": "fragility_audit", "status": "skipped_no_dataset_or_antifragile"})

    save_json(out_root / "human_learning_manifest.json", manifest)
    md = [f"# Astro Human Learning Protocol - {asset} {timeframe}\n"]
    md.append("This run is self-healing: it checked local/archive price data, fetched missing MT5 rates, checked local/archive astro data, built missing astro features, trained interpretable models, and built skeptical cognitive memory.\n")
    md.append("## Inputs resolved")
    md.append(f"- Price CSV: `{price_csv}`")
    md.append(f"- Astro CSV: `{astro_csv}`")
    md.append("\n## Steps")
    for s in manifest["steps"]:  # type: ignore[index]
        md.append(f"- `{s.get('step')}`: `{s}`")
    (out_root / "HUMAN_LEARNING_REPORT.md").write_text("\n".join(md), encoding="utf-8")

    print(f"RESOLVED_PRICE_CSV={price_csv}")
    print(f"RESOLVED_ASTRO_CSV={astro_csv}")
    print(f"HUMAN_LEARNING_PROTOCOL_ID={protocol_id}")
    print(f"HUMAN_LEARNING_PROTOCOL_DIR={out_root}")
    print(f"HUMAN_LEARNING_REPORT={out_root / 'HUMAN_LEARNING_REPORT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
