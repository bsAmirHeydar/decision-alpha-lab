#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from astro_ml_core import load_json, save_json, save_excel


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a professional model card for a saved Astro ML run.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--out-md", default="")
    ap.add_argument("--out-json", default="")
    ap.add_argument("--top-n", type=int, default=40)
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        raise FileNotFoundError(run_dir)
    metadata = load_json(run_dir / "metadata.json") if (run_dir / "metadata.json").exists() else {}
    metrics = load_json(run_dir / "metrics.json") if (run_dir / "metrics.json").exists() else metadata.get("metrics", {})
    importance = pd.read_csv(run_dir / "feature_importance.csv") if (run_dir / "feature_importance.csv").exists() else pd.DataFrame()
    top = importance.head(args.top_n).copy() if not importance.empty else pd.DataFrame()

    run_id = metadata.get("run_id", run_dir.name)
    target = metadata.get("target", "unknown")
    asset = metadata.get("asset", "unknown")
    timeframe = metadata.get("timeframe", "unknown")
    train_rows = metadata.get("train_rows", "")
    test_rows = metadata.get("test_rows", "")
    model_type = metadata.get("train_config", {}).get("model_type", "")

    card = {
        "run_id": run_id,
        "asset": asset,
        "timeframe": timeframe,
        "target": target,
        "model_type": model_type,
        "train_rows": train_rows,
        "test_rows": test_rows,
        "metrics": metrics,
        "top_features": top.to_dict(orient="records") if not top.empty else [],
        "intended_use": "Research only. Use as an interpretable astro-state learner, not as a standalone trading system.",
        "leakage_policy": "Features must be known at candle t; outcome/forward columns must not enter the feature set.",
        "validation_policy": "Chronological split and walk-forward testing must be preferred over random split.",
        "acceptance_policy": "Candidate status requires positive balanced-accuracy edge over baseline, controlled probability quality, and later walk-forward/fragility survival.",
    }

    out_md = Path(args.out_md) if args.out_md else run_dir / "MODEL_CARD.md"
    out_json = Path(args.out_json) if args.out_json else run_dir / "model_card.json"

    lines = []
    lines.append(f"# Astro ML Model Card - {run_id}\n")
    lines.append("## Identity\n")
    lines.append(f"- Asset: `{asset}`")
    lines.append(f"- Timeframe: `{timeframe}`")
    lines.append(f"- Target: `{target}`")
    lines.append(f"- Model type: `{model_type}`")
    lines.append(f"- Train rows: `{train_rows}`")
    lines.append(f"- Test rows: `{test_rows}`\n")
    lines.append("## Metrics\n")
    for k, v in metrics.items():
        if isinstance(v, (int, float, str)):
            lines.append(f"- {k}: `{v}`")
    lines.append("\n## Top learned features\n")
    if top.empty:
        lines.append("No feature importance file found.")
    else:
        for _, row in top.iterrows():
            fname = row.get("feature", row.get("transformed_feature", ""))
            imp = row.get("importance", "")
            lines.append(f"- `{fname}`: {imp}")
    lines.append("\n## Interpretation protocol\n")
    lines.append("Do not treat top features as causal proof. Treat them as hypotheses for further walk-forward and ablation testing.")
    lines.append("A model is accepted only if it beats the majority/time baseline out-of-sample and does not rely on leakage-like columns.\n")
    lines.append("## Operational status\n")
    bal = metrics.get("balanced_accuracy", 0) or 0
    edge = metrics.get("edge_over_baseline_balanced_accuracy", 0) or 0
    brier = metrics.get("brier_macro", None)
    try:
        bal_f = float(bal)
    except Exception:
        bal_f = 0.0
    try:
        edge_f = float(edge)
    except Exception:
        edge_f = 0.0
    try:
        brier_f = float(brier) if brier is not None else 999.0
    except Exception:
        brier_f = 999.0
    if bal_f >= 0.55 and edge_f >= 0.015 and brier_f <= 0.35:
        status = "candidate_for_more_oos_testing"
    elif edge_f > 0.0:
        status = "weak_candidate_requires_walk_forward_and_calibration"
    else:
        status = "research_only_not_accepted"
    lines.append(f"Status: `{status}`\n")
    lines.append(f"Balanced edge over baseline: `{edge_f}`")
    lines.append(f"Brier macro: `{brier}`\n")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    save_json(out_json, card)
    save_excel(run_dir / "model_card.xlsx", {
        "Metrics": pd.DataFrame([metrics]),
        "TopFeatures": top,
        "ModelCard": pd.DataFrame([{k: v for k, v in card.items() if k not in ("metrics", "top_features")}]),
    })

    print(f"ASTRO_ML_MODEL_CARD_MD={out_md}")
    print(f"ASTRO_ML_MODEL_CARD_JSON={out_json}")
    print(f"MODEL_STATUS={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
