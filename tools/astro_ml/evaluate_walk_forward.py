#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from astro_ml_core import (
    DEFAULT_COMMON_FILES,
    FeatureConfig,
    TrainConfig,
    aggregate_feature_importance,
    build_pipeline,
    class_probability_frame,
    ensure_dir,
    evaluate_predictions,
    infer_feature_columns,
    normalize_time_column,
    read_csv_flexible,
    save_excel,
    save_json,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run chronological walk-forward validation for Astro Meta Learner.")
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--target", default="label_direction_60")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--time-col", default="")
    ap.add_argument("--model-type", default="extra_trees", choices=["extra_trees", "random_forest", "gradient_boosting", "logit"])
    ap.add_argument("--train-days", type=int, default=120)
    ap.add_argument("--test-days", type=int, default=20)
    ap.add_argument("--step-days", type=int, default=20)
    ap.add_argument("--embargo-bars", type=int, default=120)
    ap.add_argument("--n-estimators", type=int, default=400)
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--keep-text-meta", action="store_true")
    ap.add_argument("--include-regex", default="")
    ap.add_argument("--exclude-regex", default="")
    args = ap.parse_args()

    common = Path(args.common_files)
    dataset_path = Path(args.dataset_csv)
    if not dataset_path.is_absolute():
        dataset_path = common / dataset_path
    if args.train_days <= 0 or args.test_days <= 0 or args.step_days <= 0:
        raise ValueError("train-days, test-days, and step-days must be positive.")

    df = read_csv_flexible(dataset_path)
    df, time_col = normalize_time_column(df, args.time_col or None)
    if args.target not in df.columns:
        raise ValueError(f"Target not found: {args.target}")

    feature_cfg = FeatureConfig(keep_text_meta=args.keep_text_meta, include_regex=args.include_regex or None, exclude_regex=args.exclude_regex or None)
    numeric, categorical, dropped = infer_feature_columns(df, feature_cfg, target=args.target)
    train_cfg = TrainConfig(model_type=args.model_type, target=args.target, n_estimators=args.n_estimators, max_depth=args.max_depth)

    out_dir = Path(args.out_dir) if args.out_dir else common / "astro_ml" / "reports" / args.asset / args.timeframe / f"walkforward_{args.target}"
    ensure_dir(out_dir)

    start = df[time_col].min()
    end = df[time_col].max()
    train_delta = pd.Timedelta(days=args.train_days)
    test_delta = pd.Timedelta(days=args.test_days)
    step_delta = pd.Timedelta(days=args.step_days)

    fold_rows = []
    all_pred = []
    all_imp = []
    fold = 0
    cur_train_start = start
    while True:
        train_start = cur_train_start
        train_end = train_start + train_delta
        test_start = train_end + pd.Timedelta(minutes=0)
        test_end = test_start + test_delta
        if test_start >= end:
            break
        if test_end > end:
            test_end = end
        train_mask = (df[time_col] >= train_start) & (df[time_col] < train_end)
        test_mask = (df[time_col] >= test_start) & (df[time_col] < test_end)
        train_idx = np.where(train_mask)[0]
        test_idx = np.where(test_mask)[0]
        if len(train_idx) == 0 or len(test_idx) == 0:
            cur_train_start += step_delta
            continue
        if args.embargo_bars > 0:
            max_train_idx = train_idx.max() - args.embargo_bars
            train_idx = train_idx[train_idx <= max_train_idx]
        train_df = df.iloc[train_idx].dropna(subset=[args.target]).copy()
        test_df = df.iloc[test_idx].dropna(subset=[args.target]).copy()
        if len(train_df) < 200 or len(test_df) < 20 or train_df[args.target].nunique() < 2:
            cur_train_start += step_delta
            continue

        pipe = build_pipeline(numeric, categorical, train_cfg)
        pipe.fit(train_df[numeric + categorical], train_df[args.target].astype(str))
        pred = pipe.predict(test_df[numeric + categorical])
        metrics = evaluate_predictions(test_df[args.target].astype(str), pred)
        majority = train_df[args.target].astype(str).mode().iloc[0]
        base_pred = [majority] * len(test_df)
        baseline = evaluate_predictions(test_df[args.target].astype(str), base_pred)

        fold_row = {
            "fold": fold,
            "train_start": train_start,
            "train_end": train_end,
            "test_start": test_start,
            "test_end": test_end,
            "train_rows": len(train_df),
            "test_rows": len(test_df),
            "majority_baseline": majority,
            "accuracy": metrics.get("accuracy"),
            "balanced_accuracy": metrics.get("balanced_accuracy"),
            "f1_macro": metrics.get("f1_macro"),
            "baseline_accuracy": baseline.get("accuracy"),
            "baseline_balanced_accuracy": baseline.get("balanced_accuracy"),
            "baseline_f1_macro": baseline.get("f1_macro"),
        }
        fold_rows.append(fold_row)

        proba = class_probability_frame(pipe, test_df[numeric + categorical])
        pred_df = test_df[[c for c in [time_col, "broker_time", "open", "high", "low", "close", args.target] if c in test_df.columns]].copy()
        pred_df["fold"] = fold
        pred_df["prediction"] = pred
        pred_df = pd.concat([pred_df.reset_index(drop=True), proba.reset_index(drop=True)], axis=1)
        all_pred.append(pred_df)

        imp = aggregate_feature_importance(pipe, numeric, categorical)
        if not imp.empty:
            imp["fold"] = fold
            all_imp.append(imp)

        fold += 1
        cur_train_start += step_delta

    folds = pd.DataFrame(fold_rows)
    preds = pd.concat(all_pred, ignore_index=True) if all_pred else pd.DataFrame()
    imps = pd.concat(all_imp, ignore_index=True) if all_imp else pd.DataFrame()
    if not imps.empty:
        imp_summary = imps.groupby("raw_feature", as_index=False)["importance"].agg(["mean", "std", "count"]).reset_index().sort_values("mean", ascending=False)
    else:
        imp_summary = pd.DataFrame()

    report = {
        "asset": args.asset,
        "timeframe": args.timeframe,
        "dataset_csv": str(dataset_path),
        "target": args.target,
        "time_col": time_col,
        "feature_config": asdict(feature_cfg),
        "train_config": asdict(train_cfg),
        "folds": int(len(folds)),
        "mean_accuracy": float(folds["accuracy"].mean()) if not folds.empty else None,
        "mean_balanced_accuracy": float(folds["balanced_accuracy"].mean()) if not folds.empty else None,
        "mean_f1_macro": float(folds["f1_macro"].mean()) if not folds.empty else None,
        "mean_baseline_accuracy": float(folds["baseline_accuracy"].mean()) if not folds.empty else None,
        "numeric_features": numeric,
        "categorical_features": categorical,
        "dropped_columns": dropped,
    }
    save_json(out_dir / "walkforward_report.json", report)
    folds.to_csv(out_dir / "walkforward_folds.csv", index=False, encoding="utf-8")
    preds.to_csv(out_dir / "walkforward_predictions.csv", index=False, encoding="utf-8")
    imp_summary.to_csv(out_dir / "walkforward_feature_importance.csv", index=False, encoding="utf-8")
    save_excel(out_dir / "walkforward_report.xlsx", {
        "Summary": pd.DataFrame([report]),
        "Folds": folds,
        "FeatureImportance": imp_summary,
        "Predictions": preds.head(5000),
    })
    print(f"ASTRO_ML_WALKFORWARD_DIR={out_dir}")
    print(f"FOLDS={len(folds)} MEAN_BALANCED_ACC={report['mean_balanced_accuracy']} BASELINE={report['mean_baseline_accuracy']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
