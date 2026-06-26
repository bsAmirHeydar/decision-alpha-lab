#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from astro_ml_core import (
    DEFAULT_COMMON_FILES,
    FeatureConfig,
    MemoryConfig,
    TrainConfig,
    aggregate_feature_importance,
    append_knowledge,
    append_memory_index,
    build_pipeline,
    chronological_train_test_split,
    class_probability_frame,
    ensure_dir,
    evaluate_predictions,
    generate_simple_lessons,
    infer_feature_columns,
    memory_paths,
    read_csv_flexible,
    save_excel,
    save_json,
    stable_run_id,
)

try:
    import joblib
except Exception as exc:
    raise SystemExit("joblib is required. Install with: python -m pip install joblib") from exc


def main() -> int:
    ap = argparse.ArgumentParser(description="Train an interpretable Astro Meta Learner and persist model memory.")
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--target", default="label_direction_60")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--memory-root", default="")
    ap.add_argument("--report-root", default="")
    ap.add_argument("--model-type", default="extra_trees", choices=["extra_trees", "random_forest", "gradient_boosting", "logit"])
    ap.add_argument("--test-fraction", type=float, default=0.25)
    ap.add_argument("--min-train-rows", type=int, default=1000)
    ap.add_argument("--n-estimators", type=int, default=500)
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--keep-text-meta", action="store_true")
    ap.add_argument("--max-categorical-uniques", type=int, default=64)
    ap.add_argument("--include-regex", default="")
    ap.add_argument("--exclude-regex", default="")
    args = ap.parse_args()

    common = Path(args.common_files)
    dataset_path = Path(args.dataset_csv)
    if not dataset_path.is_absolute():
        dataset_path = common / dataset_path
    df = read_csv_flexible(dataset_path)
    if args.target not in df.columns:
        raise ValueError(f"Target not found: {args.target}. Available label columns: {[c for c in df.columns if c.startswith('label_')][:30]}")

    feature_cfg = FeatureConfig(
        keep_text_meta=args.keep_text_meta,
        max_categorical_uniques=args.max_categorical_uniques,
        include_regex=args.include_regex or None,
        exclude_regex=args.exclude_regex or None,
    )
    numeric, categorical, dropped = infer_feature_columns(df, feature_cfg, target=args.target)
    train_cfg = TrainConfig(
        model_type=args.model_type,
        target=args.target,
        test_fraction=args.test_fraction,
        min_train_rows=args.min_train_rows,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
    )

    train_df, test_df = chronological_train_test_split(df, args.target, args.test_fraction)
    if len(train_df) < args.min_train_rows:
        print(f"WARNING: train rows {len(train_df)} < min_train_rows {args.min_train_rows}. Continuing for research only.")

    pipe = build_pipeline(numeric, categorical, train_cfg)
    X_train = train_df[numeric + categorical]
    y_train = train_df[args.target].astype(str)
    X_test = test_df[numeric + categorical]
    y_test = test_df[args.target].astype(str)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    metrics = evaluate_predictions(y_test, pred)
    proba = class_probability_frame(pipe, X_test)

    importance = aggregate_feature_importance(pipe, numeric, categorical)
    pred_df = test_df[[c for c in ["broker_time", "utc_time", "open", "high", "low", "close", args.target] if c in test_df.columns]].copy()
    pred_df["prediction"] = pred
    pred_df = pd.concat([pred_df.reset_index(drop=True), proba.reset_index(drop=True)], axis=1)

    mem_cfg = MemoryConfig(
        asset=args.asset,
        timeframe=args.timeframe,
        memory_root=args.memory_root or str(common / "astro_ml" / "memory"),
        report_root=args.report_root or str(common / "astro_ml" / "reports"),
    )
    run_id = stable_run_id([args.asset, args.timeframe, args.target, args.model_type, str(dataset_path)])
    paths = memory_paths(mem_cfg, run_id)
    ensure_dir(paths["run"])

    model_path = paths["run"] / "model.joblib"
    joblib.dump(pipe, model_path)

    metadata = {
        "run_id": run_id,
        "asset": args.asset,
        "timeframe": args.timeframe,
        "dataset_csv": str(dataset_path),
        "target": args.target,
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "feature_config": asdict(feature_cfg),
        "train_config": asdict(train_cfg),
        "numeric_features": numeric,
        "categorical_features": categorical,
        "dropped_columns": dropped,
        "metrics": metrics,
        "model_path": str(model_path),
    }
    save_json(paths["run"] / "metadata.json", metadata)
    save_json(paths["run"] / "metrics.json", metrics)
    importance.to_csv(paths["run"] / "feature_importance.csv", index=False, encoding="utf-8")
    pred_df.to_csv(paths["run"] / "test_predictions.csv", index=False, encoding="utf-8")
    save_excel(paths["run"] / "training_report.xlsx", {
        "Metrics": pd.DataFrame([metrics | {"target": args.target, "run_id": run_id}]),
        "FeatureImportance": importance,
        "Predictions": pred_df.head(5000),
        "FeatureSchema": pd.DataFrame([{"type": "numeric", "feature": f} for f in numeric] + [{"type": "categorical", "feature": f} for f in categorical]),
    })

    lessons = generate_simple_lessons(importance, metrics, args.target)
    save_json(paths["run"] / "knowledge_base.json", {"run_id": run_id, "lessons": lessons})
    append_knowledge(mem_cfg, run_id, lessons)
    append_memory_index(mem_cfg, run_id, {
        "asset": args.asset,
        "timeframe": args.timeframe,
        "target": args.target,
        "model_type": args.model_type,
        "train_rows": len(train_df),
        "test_rows": len(test_df),
        "accuracy": metrics.get("accuracy"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "f1_macro": metrics.get("f1_macro"),
        "run_dir": str(paths["run"]),
    })

    print(f"ASTRO_ML_RUN_ID={run_id}")
    print(f"ASTRO_ML_RUN_DIR={paths['run']}")
    print(f"ASTRO_ML_MODEL={model_path}")
    print(f"ACCURACY={metrics.get('accuracy')} BALANCED_ACCURACY={metrics.get('balanced_accuracy')} F1_MACRO={metrics.get('f1_macro')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
