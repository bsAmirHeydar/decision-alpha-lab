#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, class_probability_frame, load_json, read_csv_flexible, save_excel

try:
    import joblib
except Exception as exc:
    raise SystemExit("joblib is required. Install with: python -m pip install joblib") from exc


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply a saved Astro Meta Learner memory/model to a new dataset.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--out-csv", default="")
    ap.add_argument("--out-xlsx", default="")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    args = ap.parse_args()

    common = Path(args.common_files)
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = common / run_dir
    meta = load_json(run_dir / "metadata.json")
    model_path = Path(meta.get("model_path", run_dir / "model.joblib"))
    if not model_path.exists():
        model_path = run_dir / "model.joblib"
    pipe = joblib.load(model_path)

    dataset = Path(args.dataset_csv)
    if not dataset.is_absolute():
        dataset = common / dataset
    df = read_csv_flexible(dataset)
    features = meta["numeric_features"] + meta["categorical_features"]
    missing = [f for f in features if f not in df.columns]
    if missing:
        raise ValueError(f"Prediction dataset is missing {len(missing)} trained features. First missing: {missing[:10]}")
    X = df[features]
    pred = pipe.predict(X)
    proba = class_probability_frame(pipe, X)
    keep_cols = [c for c in ["broker_time", "utc_time", "open", "high", "low", "close", meta.get("target")] if c in df.columns]
    out = df[keep_cols].copy()
    out["prediction"] = pred
    out = pd.concat([out.reset_index(drop=True), proba.reset_index(drop=True)], axis=1)

    out_csv = Path(args.out_csv) if args.out_csv else dataset.with_name(dataset.stem + f"_pred_{meta['target']}.csv")
    if not out_csv.is_absolute():
        out_csv = common / out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False, encoding="utf-8")
    out_xlsx = Path(args.out_xlsx) if args.out_xlsx else out_csv.with_suffix(".xlsx")
    if not out_xlsx.is_absolute():
        out_xlsx = common / out_xlsx
    save_excel(out_xlsx, {"Predictions": out.head(100000), "RunMetadata": pd.DataFrame([meta])})
    print(f"ASTRO_ML_PREDICTIONS_CSV={out_csv}")
    print(f"ASTRO_ML_PREDICTIONS_XLSX={out_xlsx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
