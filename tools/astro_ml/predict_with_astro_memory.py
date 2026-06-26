#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, class_probability_frame, load_json, read_csv_flexible, save_excel

try:
    import joblib
except Exception as exc:
    raise SystemExit("joblib is required. Install with: python -m pip install joblib") from exc


def discover_latest_decision_memory(common: Path, asset: str, timeframe: str) -> Path | None:
    root = common / "astro_ml" / "antifragile_fragility_audits" / asset.upper() / timeframe.upper()
    if not root.exists():
        return None
    hits = sorted(root.glob("*/antifragile_decision_memory.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return hits[0] if hits else None


def principle_state_match(series: pd.Series, state: str, q33: float | None, q67: float | None) -> pd.Series:
    vals = pd.to_numeric(series, errors="coerce")
    if state == "LOW" and q33 is not None:
        return vals <= q33
    if state == "HIGH" and q67 is not None:
        return vals >= q67
    if state == "MID" and q33 is not None and q67 is not None:
        return (vals > q33) & (vals < q67)
    return pd.Series(False, index=series.index)


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply a saved Astro Meta Learner memory/model to a new dataset.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--out-csv", default="")
    ap.add_argument("--out-xlsx", default="")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--decision-memory-json", default="", help="Optional fragility-audit decision memory. Default = latest for asset/timeframe.")
    ap.add_argument("--allow-research-model", action="store_true", help="Allow prediction even when model/decision memory is still research-only.")
    args = ap.parse_args()

    common = Path(args.common_files)
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = common / run_dir
    meta = load_json(run_dir / "metadata.json")
    model_card = load_json(run_dir / "model_card.json") if (run_dir / "model_card.json").exists() else {}
    model_path = Path(meta.get("model_path", run_dir / "model.joblib"))
    if not model_path.exists():
        model_path = run_dir / "model.joblib"
    pipe = joblib.load(model_path)

    dataset = Path(args.dataset_csv)
    if not dataset.is_absolute():
        dataset = common / dataset
    df = read_csv_flexible(dataset)
    asset = str(meta.get("asset", "NAS100"))
    timeframe = str(meta.get("timeframe", "M1"))
    decision_memory_path = Path(args.decision_memory_json) if args.decision_memory_json else discover_latest_decision_memory(common, asset, timeframe)
    if decision_memory_path and not decision_memory_path.is_absolute():
        decision_memory_path = common / decision_memory_path
    decision_memory = load_json(decision_memory_path) if decision_memory_path and decision_memory_path.exists() else {}
    production_gate = str(decision_memory.get("production_gate", "unknown")) if decision_memory else "unknown"
    model_status = str(model_card.get("status", "unknown")) if model_card else "unknown"
    target_name = str(meta.get("target", ""))
    hardened = [x for x in (decision_memory.get("hardened_principles", []) if decision_memory else []) if str(x.get("target", "")) == target_name]
    target_gate = "pass" if production_gate == "pass" and len(hardened) > 0 else ("research_only" if decision_memory else "unknown")
    if not args.allow_research_model:
        if model_status in {"research_only_not_accepted", "weak_candidate_requires_walk_forward_and_calibration"}:
            raise SystemExit(f"Model card status is {model_status}. Use --allow-research-model to force prediction.")
        if target_gate == "research_only":
            raise SystemExit("Latest fragility decision memory does not grant a hardened pass for this target. Use --allow-research-model to force prediction.")

    source = df.reset_index(drop=True).copy()
    features = meta["numeric_features"] + meta["categorical_features"]
    missing = [f for f in features if f not in df.columns]
    if missing:
        raise ValueError(f"Prediction dataset is missing {len(missing)} trained features. First missing: {missing[:10]}")
    X = source[features]
    pred = pipe.predict(X)
    proba = class_probability_frame(pipe, X)
    keep_cols = [c for c in ["broker_time", "utc_time", "open", "high", "low", "close", meta.get("target")] if c in df.columns]
    out = source[keep_cols].copy()
    out["prediction"] = pred
    out = pd.concat([out.reset_index(drop=True), proba.reset_index(drop=True)], axis=1)
    if not proba.empty:
        p = proba.to_numpy(dtype=float)
        p_sorted = -np.sort(-p, axis=1)
        out["prediction_confidence"] = p_sorted[:, 0]
        out["prediction_margin"] = p_sorted[:, 0] - p_sorted[:, 1] if p_sorted.shape[1] > 1 else p_sorted[:, 0]
    else:
        out["prediction_confidence"] = np.nan
        out["prediction_margin"] = np.nan

    out["model_status"] = model_status
    out["production_gate"] = target_gate
    out["hardened_support_count"] = 0
    out["hardened_conflict_count"] = 0

    if hardened:
        for item in hardened:
            feature = str(item.get("feature", ""))
            state = str(item.get("state", ""))
            positive_label = str(item.get("positive_label", ""))
            if feature not in source.columns:
                continue
            try:
                q33 = float(item.get("q33")) if item.get("q33") is not None else None
            except Exception:
                q33 = None
            try:
                q67 = float(item.get("q67")) if item.get("q67") is not None else None
            except Exception:
                q67 = None
            mask = principle_state_match(source[feature], state, q33, q67)
            support_mask = mask & out["prediction"].astype(str).eq(positive_label)
            conflict_mask = mask & ~out["prediction"].astype(str).eq(positive_label)
            out.loc[support_mask, "hardened_support_count"] += 1
            out.loc[conflict_mask, "hardened_conflict_count"] += 1

    out["trust_tier"] = "research"
    high_guard = (
        out["production_gate"].astype(str).eq("pass")
        & (out["hardened_support_count"] >= 1)
        & (out["hardened_conflict_count"] == 0)
        & (out["prediction_confidence"] >= 0.60)
    )
    medium_guard = (
        (out["prediction_confidence"] >= 0.50)
        & (out["prediction_margin"] >= 0.08)
        & (out["hardened_conflict_count"] <= 1)
    )
    out.loc[medium_guard, "trust_tier"] = "candidate"
    out.loc[high_guard, "trust_tier"] = "hardened_candidate"

    out_csv = Path(args.out_csv) if args.out_csv else dataset.with_name(dataset.stem + f"_pred_{meta['target']}.csv")
    if not out_csv.is_absolute():
        out_csv = common / out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False, encoding="utf-8")
    out_xlsx = Path(args.out_xlsx) if args.out_xlsx else out_csv.with_suffix(".xlsx")
    if not out_xlsx.is_absolute():
        out_xlsx = common / out_xlsx
    meta_sheet = pd.DataFrame([{
        **meta,
        "model_status": model_status,
        "decision_memory_json": str(decision_memory_path) if decision_memory_path else "",
        "production_gate": target_gate,
        "hardened_principles_count": len(hardened),
    }])
    hardened_df = pd.DataFrame(hardened)
    save_excel(out_xlsx, {"Predictions": out.head(100000), "RunMetadata": meta_sheet, "HardenedPrinciples": hardened_df})
    print(f"ASTRO_ML_PREDICTIONS_CSV={out_csv}")
    print(f"ASTRO_ML_PREDICTIONS_XLSX={out_xlsx}")
    print(f"ASTRO_ML_MODEL_STATUS={model_status}")
    print(f"ASTRO_ML_PRODUCTION_GATE={target_gate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
