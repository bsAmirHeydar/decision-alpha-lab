#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, load_json, read_csv_flexible, save_excel, save_json


def numeric_rule_scan(df: pd.DataFrame, features, target: str, positive_label: str, max_features: int = 25):
    rows = []
    for f in features[:max_features]:
        if f not in df.columns or not pd.api.types.is_numeric_dtype(df[f]):
            continue
        s = pd.to_numeric(df[f], errors="coerce")
        try:
            q = pd.qcut(s, 5, duplicates="drop")
        except Exception:
            continue
        tmp = pd.DataFrame({"bucket": q, "target": df[target].astype(str)})
        g = tmp.dropna().groupby("bucket")
        for bucket, part in g:
            n = len(part)
            if n < 20:
                continue
            rate = (part["target"] == positive_label).mean()
            rows.append({"feature": f, "bucket": str(bucket), "n": int(n), "positive_label": positive_label, "positive_rate": float(rate)})
    return pd.DataFrame(rows).sort_values("positive_rate", ascending=False) if rows else pd.DataFrame()


def categorical_rule_scan(df: pd.DataFrame, features, target: str, positive_label: str, max_features: int = 25):
    rows = []
    for f in features[:max_features]:
        if f not in df.columns or pd.api.types.is_numeric_dtype(df[f]):
            continue
        vc = df[f].astype(str).value_counts().head(20).index
        for value in vc:
            part = df[df[f].astype(str) == value]
            n = len(part)
            if n < 20:
                continue
            rate = (part[target].astype(str) == positive_label).mean()
            rows.append({"feature": f, "value": value, "n": int(n), "positive_label": positive_label, "positive_rate": float(rate)})
    return pd.DataFrame(rows).sort_values("positive_rate", ascending=False) if rows else pd.DataFrame()


def main() -> int:
    ap = argparse.ArgumentParser(description="Explain an Astro Meta Learner run and extract reusable mechanical astro rules.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--dataset-csv", default="", help="Optional dataset CSV for rule scan. Defaults to metadata dataset.")
    ap.add_argument("--positive-label", default="", help="Label to scan for. Defaults UP for direction, SPIKE for spike, trap label for trap.")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = Path(args.common_files) / run_dir
    meta = load_json(run_dir / "metadata.json")
    imp_path = run_dir / "feature_importance.csv"
    importance = pd.read_csv(imp_path) if imp_path.exists() else pd.DataFrame()
    dataset_path = Path(args.dataset_csv or meta.get("dataset_csv"))
    if not dataset_path.is_absolute():
        dataset_path = Path(args.common_files) / dataset_path
    df = read_csv_flexible(dataset_path)
    target = meta["target"]
    if target not in df.columns:
        raise ValueError(f"Target not found in dataset: {target}")
    if args.positive_label:
        pos = args.positive_label
    elif "direction" in target:
        pos = "UP"
    elif "spike" in target:
        pos = "SPIKE"
    elif "bull_trap" in target:
        pos = "BULL_TRAP"
    elif "bear_trap" in target:
        pos = "BEAR_TRAP"
    elif "clean_long" in target:
        pos = "CLEAN_LONG"
    elif "clean_short" in target:
        pos = "CLEAN_SHORT"
    else:
        pos = str(df[target].astype(str).mode().iloc[0])

    top_features = importance["raw_feature"].head(40).tolist() if not importance.empty else meta.get("numeric_features", [])[:40]
    num_rules = numeric_rule_scan(df, top_features, target, pos)
    cat_rules = categorical_rule_scan(df, top_features, target, pos)

    lessons = []
    for _, r in num_rules.head(20).iterrows():
        lessons.append({
            "lesson_type": "numeric_rule",
            "target": target,
            "positive_label": pos,
            "feature": r["feature"],
            "condition": r["bucket"],
            "n": int(r["n"]),
            "positive_rate": float(r["positive_rate"]),
            "interpretation": f"When {r['feature']} is in {r['bucket']}, {pos} occurred at rate {r['positive_rate']:.3f} in this dataset slice.",
        })
    for _, r in cat_rules.head(20).iterrows():
        lessons.append({
            "lesson_type": "categorical_rule",
            "target": target,
            "positive_label": pos,
            "feature": r["feature"],
            "condition": str(r["value"]),
            "n": int(r["n"]),
            "positive_rate": float(r["positive_rate"]),
            "interpretation": f"When {r['feature']} equals {r['value']}, {pos} occurred at rate {r['positive_rate']:.3f} in this dataset slice.",
        })

    out_json = run_dir / "extracted_rules.json"
    save_json(out_json, {"target": target, "positive_label": pos, "lessons": lessons})
    save_excel(run_dir / "explainability_report.xlsx", {
        "FeatureImportance": importance,
        "NumericRules": num_rules,
        "CategoricalRules": cat_rules,
        "Lessons": pd.DataFrame(lessons),
    })
    print(f"ASTRO_ML_EXPLAIN_DIR={run_dir}")
    print(f"RULES_JSON={out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
