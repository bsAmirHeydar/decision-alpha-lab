#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, FeatureConfig, ensure_dir, infer_feature_columns, read_csv_flexible, save_excel, save_json


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
    ap.add_argument("--fail-on-critical", action="store_true", help="Exit non-zero when critical data-quality gates fail.")
    ap.add_argument("--min-rows", type=int, default=1000)
    ap.add_argument("--max-target-majority-pct", type=float, default=0.985)
    ap.add_argument("--max-feature-missing-pct", type=float, default=0.50)
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
    numeric_features, categorical_features, dropped_features = infer_feature_columns(df, FeatureConfig())
    usable_features = set(numeric_features + categorical_features)
    leakage_in_features = leaks[leaks["column"].isin(usable_features)].copy() if not leaks.empty else pd.DataFrame()
    constant_cols = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]
    constants = pd.DataFrame({"column": constant_cols})

    critical_rows = []
    warning_rows = []
    if len(df) < args.min_rows:
        critical_rows.append({"gate": "min_rows", "value": len(df), "limit": args.min_rows, "reason": "dataset_too_small_for_stable_learning"})
    if time_col is None:
        critical_rows.append({"gate": "time_column", "value": "missing", "limit": "required", "reason": "chronological_validation_requires_time"})
    if not gap_summary.empty:
        gap_spikes = int(gap_summary.loc[gap_summary["metric"].eq("gaps_gt_5x_median"), "value"].iloc[0])
        if gap_spikes > max(10, int(len(df) * 0.002)):
            warning_rows.append({"gate": "time_gaps", "value": gap_spikes, "limit": max(10, int(len(df) * 0.002)), "reason": "many_large_time_gaps"})
    if not leakage_in_features.empty:
        critical_rows.append({"gate": "leakage_feature_names", "value": len(leakage_in_features), "limit": 0, "reason": "outcome_like_columns_entered_feature_set"})

    if not labels.empty:
        maj = labels.groupby("target", as_index=False)["majority_baseline_for_target"].max()
        for _, r in maj.iterrows():
            if float(r["majority_baseline_for_target"]) >= args.max_target_majority_pct:
                critical_rows.append({"gate": "target_majority_pct", "target": r["target"], "value": float(r["majority_baseline_for_target"]), "limit": args.max_target_majority_pct, "reason": "target_too_imbalanced_to_trust"})
    high_missing_features = missing[(missing["column"].isin(usable_features)) & (missing["missing_pct"] > args.max_feature_missing_pct)]
    if not high_missing_features.empty:
        warning_rows.append({"gate": "feature_missing_pct", "value": int(len(high_missing_features)), "limit": args.max_feature_missing_pct, "reason": "usable_features_have_high_missingness"})

    gate_summary = pd.DataFrame(critical_rows + warning_rows)
    critical_count = len(critical_rows)
    warning_count = len(warning_rows)

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
        "LeakageInUsableFeatures": leakage_in_features,
        "ConstantColumns": constants,
        "QualityGates": gate_summary,
    })
    save_json(out_json, {
        "asset": args.asset,
        "timeframe": args.timeframe,
        "dataset": str(dataset_path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "targets": target_cols(df),
        "leakage_name_candidates": leaks.to_dict(orient="records"),
        "leakage_in_usable_features": leakage_in_features.to_dict(orient="records") if not leakage_in_features.empty else [],
        "constant_columns": constant_cols[:500],
        "usable_numeric_features": len(numeric_features),
        "usable_categorical_features": len(categorical_features),
        "dropped_features": len(dropped_features),
        "critical_gate_failures": critical_rows,
        "warning_gate_flags": warning_rows,
        "critical_count": critical_count,
        "warning_count": warning_count,
    })

    print(f"ASTRO_ML_AUDIT_XLSX={out_xlsx}")
    print(f"ASTRO_ML_AUDIT_JSON={out_json}")
    print(f"ROWS={len(df)} TARGETS={len(target_cols(df))} LEAKAGE_NAME_CANDIDATES={len(leaks)} CRITICAL_GATES={critical_count} WARNING_GATES={warning_count}")
    if args.fail_on_critical and critical_count > 0:
        raise SystemExit(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
