#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, read_csv_flexible, save_excel, save_json


def resolve_common_path(path_text: str, common: Path) -> Path:
    p = Path(path_text)
    return p if p.is_absolute() else common / p


def target_cols(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if c.startswith("label_")]


def leakage_candidates(df: pd.DataFrame) -> pd.DataFrame:
    bad_tokens = ["future_", "ret_", "mfe_", "mae_", "label_", "target_", "outcome_", "clean_", "trap_", "spike_"]
    rows = []
    for c in df.columns:
        low = c.lower()
        hits = [t for t in bad_tokens if low.startswith(t) or t in low]
        if hits:
            rows.append({"column": c, "reason": ",".join(hits)})
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit an EXP0016 Astro ML dataset before training.")
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--out-xlsx", default="")
    ap.add_argument("--out-json", default="")
    args = ap.parse_args()

    common = Path(args.common_files)
    dataset_path = resolve_common_path(args.dataset_csv, common)
    if not dataset_path.exists():
        raise FileNotFoundError(dataset_path)
    df = read_csv_flexible(dataset_path)

    time_col = None
    for c in ["broker_time", "time", "datetime", "timestamp", "utc_time", "open_time", "candle_time"]:
        if c in df.columns:
            time_col = c
            break
    time_summary = []
    gap_summary = pd.DataFrame()
    if time_col:
        t = pd.to_datetime(df[time_col], errors="coerce")
        valid = t.dropna().sort_values()
        time_summary = [
            {"key": "time_col", "value": time_col},
            {"key": "start", "value": str(valid.iloc[0]) if len(valid) else ""},
            {"key": "end", "value": str(valid.iloc[-1]) if len(valid) else ""},
            {"key": "valid_time_rows", "value": int(len(valid))},
        ]
        if len(valid) > 2:
            gaps = valid.diff().dropna().dt.total_seconds()
            gap_summary = pd.DataFrame([
                {"metric": "median_gap_seconds", "value": float(gaps.median())},
                {"metric": "p95_gap_seconds", "value": float(gaps.quantile(0.95))},
                {"metric": "max_gap_seconds", "value": float(gaps.max())},
                {"metric": "gaps_gt_5x_median", "value": int((gaps > max(gaps.median() * 5, 1)).sum())},
            ])

    summary = pd.DataFrame([
        {"key": "asset", "value": args.asset},
        {"key": "timeframe", "value": args.timeframe},
        {"key": "dataset", "value": str(dataset_path)},
        {"key": "rows", "value": int(len(df))},
        {"key": "columns", "value": int(len(df.columns))},
        {"key": "targets", "value": int(len(target_cols(df)))},
    ] + time_summary)

    missing = pd.DataFrame({
        "column": df.columns,
        "missing_count": [int(df[c].isna().sum()) for c in df.columns],
        "missing_pct": [float(df[c].isna().mean()) for c in df.columns],
        "unique_count": [int(df[c].nunique(dropna=True)) for c in df.columns],
    }).sort_values(["missing_pct", "unique_count"], ascending=[False, True])

    label_rows = []
    for c in target_cols(df):
        vc = df[c].value_counts(dropna=False)
        total = max(len(df), 1)
        majority = float(vc.iloc[0] / total) if len(vc) else 0.0
        entropy = 0.0
        for count in vc.values:
            p = float(count / total)
            if p > 0:
                entropy -= p * np.log2(p)
        for label, count in vc.items():
            label_rows.append({
                "target": c,
                "label": str(label),
                "count": int(count),
                "pct": float(count / total),
                "majority_baseline_for_target": majority,
                "entropy": entropy,
            })
    labels = pd.DataFrame(label_rows)

    leaks = leakage_candidates(df)
    constant_cols = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]
    constants = pd.DataFrame({"column": constant_cols})

    report_dir = common / "astro_ml" / "reports" / args.asset / args.timeframe
    ensure_dir(report_dir)
    out_xlsx = Path(args.out_xlsx) if args.out_xlsx else report_dir / f"astro_ml_dataset_audit_{args.asset}_{args.timeframe}.xlsx"
    if not out_xlsx.is_absolute():
        out_xlsx = common / out_xlsx
    out_json = Path(args.out_json) if args.out_json else out_xlsx.with_suffix(".json")
    if not out_json.is_absolute():
        out_json = common / out_json

    save_excel(out_xlsx, {
        "Summary": summary,
        "LabelDistribution": labels,
        "MissingAndUnique": missing.head(5000),
        "TimeGaps": gap_summary,
        "LeakageNameCandidates": leaks,
        "ConstantColumns": constants,
    })
    save_json(out_json, {
        "asset": args.asset,
        "timeframe": args.timeframe,
        "dataset": str(dataset_path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "targets": target_cols(df),
        "leakage_name_candidates": leaks.to_dict(orient="records"),
        "constant_columns": constant_cols[:500],
    })

    print(f"ASTRO_ML_AUDIT_XLSX={out_xlsx}")
    print(f"ASTRO_ML_AUDIT_JSON={out_json}")
    print(f"ROWS={len(df)} TARGETS={len(target_cols(df))} LEAKAGE_NAME_CANDIDATES={len(leaks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
