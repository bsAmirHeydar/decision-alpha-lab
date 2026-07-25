#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from astro_ml_core import (
    DEFAULT_COMMON_FILES,
    DEFAULT_REPORT_ROOT,
    FeatureConfig,
    OutcomeConfig,
    add_future_outcomes,
    ensure_dir,
    infer_feature_columns,
    merge_astro_price,
    normalize_time_column,
    read_csv_flexible,
    save_excel,
    save_json,
)


def parse_horizons(raw: str):
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a causal Astro ML dataset by joining mechanical astro features with future market outcomes.")
    ap.add_argument("--astro-csv", required=True, help="Astro feature CSV. May be an absolute path or a Common\\Files filename.")
    ap.add_argument("--price-csv", default="", help="Optional OHLC CSV to merge by time. If absent, astro CSV must contain OHLC columns.")
    ap.add_argument("--out-csv", default="", help="Output dataset CSV. Default: Common\\Files\\astro_ml\\reports\\...")
    ap.add_argument("--out-xlsx", default="", help="Optional output Excel summary.")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--time-col", default="", help="Astro time column, default auto-detect.")
    ap.add_argument("--price-time-col", default="", help="Price time column, default auto-detect.")
    ap.add_argument("--merge-tolerance", default="30s")
    ap.add_argument("--horizons", default="30,60,120")
    ap.add_argument("--direction-threshold-pct", type=float, default=0.0010)
    ap.add_argument("--spike-threshold-pct", type=float, default=0.0030)
    ap.add_argument("--trap-trigger-pct", type=float, default=0.0015)
    ap.add_argument("--clean-min-mfe-pct", type=float, default=0.0015)
    ap.add_argument("--clean-max-mae-pct", type=float, default=0.0008)
    ap.add_argument("--keep-text-meta", action="store_true")
    ap.add_argument("--max-categorical-uniques", type=int, default=64)
    args = ap.parse_args()

    common = Path(args.common_files)
    astro_path = Path(args.astro_csv)
    if not astro_path.is_absolute():
        astro_path = common / astro_path
    if not astro_path.exists():
        raise FileNotFoundError(astro_path)

    price_path = Path(args.price_csv) if args.price_csv else None
    if price_path is not None and not price_path.is_absolute():
        price_path = common / price_path
    if price_path is not None and not price_path.exists():
        raise FileNotFoundError(price_path)

    astro_df = read_csv_flexible(astro_path)
    astro_df, astro_time_col = normalize_time_column(astro_df, args.time_col or None)
    price_df = read_csv_flexible(price_path) if price_path else None
    merged, price_cols = merge_astro_price(astro_df, price_df, astro_time_col, args.price_time_col or None, args.merge_tolerance)

    outcome_cfg = OutcomeConfig(
        horizons=parse_horizons(args.horizons),
        direction_threshold_pct=args.direction_threshold_pct,
        spike_threshold_pct=args.spike_threshold_pct,
        trap_trigger_pct=args.trap_trigger_pct,
        clean_min_mfe_pct=args.clean_min_mfe_pct,
        clean_max_mae_pct=args.clean_max_mae_pct,
    )
    dataset = add_future_outcomes(merged, price_cols, outcome_cfg)

    feature_cfg = FeatureConfig(keep_text_meta=args.keep_text_meta, max_categorical_uniques=args.max_categorical_uniques)
    numeric, categorical, dropped = infer_feature_columns(dataset, feature_cfg)

    reports = Path(DEFAULT_REPORT_ROOT) / args.asset / args.timeframe
    ensure_dir(reports)
    out_csv = Path(args.out_csv) if args.out_csv else reports / f"astro_ml_dataset_{args.asset}_{args.timeframe}.csv"
    if not out_csv.is_absolute():
        out_csv = common / out_csv
    ensure_dir(out_csv.parent)
    dataset.to_csv(out_csv, index=False, encoding="utf-8")

    schema = {
        "asset": args.asset,
        "timeframe": args.timeframe,
        "astro_csv": str(astro_path),
        "price_csv": str(price_path) if price_path else "embedded_in_astro_csv",
        "rows": int(len(dataset)),
        "columns": int(len(dataset.columns)),
        "time_col": astro_time_col,
        "price_cols": price_cols,
        "outcome_config": asdict(outcome_cfg),
        "feature_config": asdict(feature_cfg),
        "numeric_features": numeric,
        "categorical_features": categorical,
        "dropped_columns": dropped,
    }
    schema_path = out_csv.with_suffix(".schema.json")
    save_json(schema_path, schema)

    label_cols = [c for c in dataset.columns if c.startswith("label_")]
    label_summary_rows = []
    for c in label_cols:
        vc = dataset[c].value_counts(dropna=False)
        for label, count in vc.items():
            label_summary_rows.append({"target": c, "label": label, "count": int(count), "pct": float(count / max(len(dataset), 1))})
    label_summary = pd.DataFrame(label_summary_rows)

    summary = pd.DataFrame([
        {"key": "asset", "value": args.asset},
        {"key": "timeframe", "value": args.timeframe},
        {"key": "rows", "value": len(dataset)},
        {"key": "columns", "value": len(dataset.columns)},
        {"key": "numeric_features", "value": len(numeric)},
        {"key": "categorical_features", "value": len(categorical)},
        {"key": "out_csv", "value": str(out_csv)},
        {"key": "schema", "value": str(schema_path)},
    ])
    if args.out_xlsx:
        xlsx = Path(args.out_xlsx)
        if not xlsx.is_absolute():
            xlsx = reports / xlsx
    else:
        xlsx = out_csv.with_suffix(".xlsx")
    save_excel(xlsx, {
        "Summary": summary,
        "LabelDistribution": label_summary,
        "FeatureSchema": pd.DataFrame([{"type": "numeric", "feature": f} for f in numeric] + [{"type": "categorical", "feature": f} for f in categorical]),
        "Sample": dataset.head(500),
    })

    print(f"ASTRO_ML_DATASET_CSV={out_csv}")
    print(f"ASTRO_ML_SCHEMA_JSON={schema_path}")
    print(f"ASTRO_ML_SUMMARY_XLSX={xlsx}")
    print(f"ROWS={len(dataset)} NUMERIC_FEATURES={len(numeric)} CATEGORICAL_FEATURES={len(categorical)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
