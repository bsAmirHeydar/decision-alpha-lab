#!/usr/bin/env python3
"""
EXP0016 - Antifragile Astro Learning Layer.

This module sits above the ordinary supervised learner. Its job is NOT to find
more conditions. Its job is to compress mechanical astro features into broad
concepts, test whether simple principles survive out-of-sample, reject fragile
patterns, and write a portable "mind" report.

Design:
- principles before details
- simple before complex
- multi-hypothesis before one forced forecast
- train/test time split only
- rules must survive OOS and complexity penalties
- neural nets are allowed only as challengers, never as unquestioned truth
"""
from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from astro_ml_core import ensure_dir, read_csv_flexible, normalize_time_column, stable_run_id, DEFAULT_COMMON_FILES

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, HistGradientBoostingClassifier


@dataclass
class AntifragileConfig:
    test_fraction: float = 0.25
    min_train_rows: int = 800
    min_rule_support: int = 120
    min_oos_support: int = 40
    min_lift: float = 1.08
    max_gap: float = 0.14
    max_principles_per_target: int = 25
    max_raw_features: int = 80
    max_concept_features: int = 80
    min_edge_over_baseline: float = 0.015
    complexity_penalty_per_feature: float = 0.0015
    neural_min_rows: int = 8000
    random_state: int = 42


CONCEPT_FAMILIES: Dict[str, Sequence[str]] = {
    # Broad causal ideas. Additive details should be folded into these unless a
    # detail proves repeatedly stable.
    "benefic_expansion": ["jupiter", "venus", "benefic", "lift", "support", "expansion", "flow"],
    "malefic_pressure": ["saturn", "mars_saturn", "malefic", "pressure", "drag", "resistance", "compression"],
    "mars_impulse": ["mars", "impulse", "drive", "fire", "aggression"],
    "lunar_timing": ["moon", "lunar", "void", "phase", "ingress"],
    "mercury_noise": ["mercury", "news", "noise", "mind", "communication"],
    "pluto_extreme": ["pluto", "extreme", "depth", "obsession", "power"],
    "uranus_shock": ["uranus", "shock", "surprise", "break", "disruption"],
    "neptune_fog": ["neptune", "fog", "confusion", "illusion", "blur"],
    "natal_activation": ["natal", "birth", "radix"],
    "aspect_tension": ["square", "opposition", "conjunction", "hard", "orb", "aspect", "declination"],
    "aspect_harmony": ["trine", "sextile", "parallel", "harmony"],
    "house_context": ["house", "angular", "cadent", "succedent"],
    "market_quality": ["path", "clean", "friction", "exhaust", "volatility", "spike", "timing", "score"],
    "directional_bias": ["long_bias", "short_bias", "macro", "direction", "bias", "align"],
}

DETAIL_BLACKLIST = re.compile(r"^(label_|ret_|mfe_|mae_|future_|target_|outcome_|open$|high$|low$|close$|tick_volume$|volume$)", re.I)
TIME_LIKE = re.compile(r"(time|date|timestamp|utc|unix|jd)", re.I)


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def save_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def numeric_feature_columns(df: pd.DataFrame) -> List[str]:
    cols: List[str] = []
    for c in df.columns:
        s = str(c)
        if DETAIL_BLACKLIST.search(s) or TIME_LIKE.search(s):
            continue
        if pd.api.types.is_numeric_dtype(df[c]):
            if df[c].notna().sum() > 10 and df[c].nunique(dropna=True) > 1:
                cols.append(c)
    return cols


def target_columns(df: pd.DataFrame, targets: str) -> List[str]:
    if targets.strip():
        out = [x.strip() for x in targets.split(",") if x.strip()]
        return [x for x in out if x in df.columns]
    preferred = [
        "label_direction_30", "label_direction_60", "label_direction_120",
        "label_clean_long_60", "label_clean_short_60",
        "label_spike_60", "label_bull_trap_60", "label_bear_trap_60",
    ]
    found = [c for c in preferred if c in df.columns]
    if found:
        return found
    return [c for c in df.columns if str(c).startswith("label_")][:8]


def match_family(col: str) -> List[str]:
    low = col.lower()
    hits = []
    for fam, keys in CONCEPT_FAMILIES.items():
        if any(k in low for k in keys):
            hits.append(fam)
    return hits or ["misc_mechanical"]


def build_concept_frame(df: pd.DataFrame, raw_cols: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    family_to_cols: Dict[str, List[str]] = {}
    for c in raw_cols:
        for fam in match_family(str(c)):
            family_to_cols.setdefault(fam, []).append(c)
            rows.append({"feature": c, "concept_family": fam})
    mapping = pd.DataFrame(rows)

    out = pd.DataFrame(index=df.index)
    for fam, cols in sorted(family_to_cols.items()):
        vals = df[cols].apply(pd.to_numeric, errors="coerce")
        # robust row-wise summaries; the model sees the principle, not every leaf.
        out[f"concept__{fam}__mean"] = vals.mean(axis=1)
        out[f"concept__{fam}__max"] = vals.max(axis=1)
        out[f"concept__{fam}__min"] = vals.min(axis=1)
        out[f"concept__{fam}__std"] = vals.std(axis=1)
        out[f"concept__{fam}__active_count"] = vals.gt(vals.median(axis=0), axis=1).sum(axis=1)
    return out, mapping


def chronological_split(df: pd.DataFrame, target: str, test_fraction: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    d = df.dropna(subset=[target]).copy()
    if d.empty:
        return d, d
    n_test = max(1, int(len(d) * test_fraction))
    if n_test >= len(d):
        n_test = max(1, len(d)//4)
    return d.iloc[:-n_test].copy(), d.iloc[-n_test:].copy()


def baseline_score(y_train: Sequence[str], y_test: Sequence[str]) -> Dict[str, float | str]:
    if len(y_train) == 0 or len(y_test) == 0:
        return {"baseline_label": "", "baseline_accuracy": np.nan, "baseline_balanced_accuracy": np.nan}
    mode = pd.Series(y_train).mode()
    label = str(mode.iloc[0]) if not mode.empty else str(y_train[0])
    pred = np.array([label] * len(y_test))
    return {
        "baseline_label": label,
        "baseline_accuracy": float(accuracy_score(y_test, pred)),
        "baseline_balanced_accuracy": float(balanced_accuracy_score(y_test, pred)),
    }


def make_pipeline(model_name: str, n_features: int, cfg: AntifragileConfig) -> Pipeline:
    if model_name == "occam_l1_logistic":
        model = LogisticRegression(
            penalty="l1", solver="liblinear", class_weight="balanced", C=0.35,
            max_iter=800, random_state=cfg.random_state,
        )
        return Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler()), ("model", model)])
    if model_name == "shallow_tree":
        model = DecisionTreeClassifier(max_depth=3, min_samples_leaf=max(20, int(0.02 * max(1, n_features))), class_weight="balanced", random_state=cfg.random_state)
        return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", model)])
    if model_name == "small_forest":
        model = RandomForestClassifier(n_estimators=250, max_depth=4, min_samples_leaf=30, class_weight="balanced_subsample", random_state=cfg.random_state, n_jobs=-1)
        return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", model)])
    if model_name == "extra_trees_challenger":
        model = ExtraTreesClassifier(n_estimators=400, max_depth=6, min_samples_leaf=20, class_weight="balanced", random_state=cfg.random_state, n_jobs=-1)
        return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", model)])
    if model_name == "neural_challenger":
        model = MLPClassifier(hidden_layer_sizes=(48, 16), activation="relu", alpha=0.01, early_stopping=True, validation_fraction=0.20, max_iter=250, random_state=cfg.random_state)
        return Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler()), ("model", model)])
    # histogram boosting can be useful, but is still a challenger.
    model = HistGradientBoostingClassifier(max_iter=180, max_leaf_nodes=12, l2_regularization=0.2, random_state=cfg.random_state)
    return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", model)])


def nonzero_complexity(pipe: Pipeline, feature_names: List[str]) -> Tuple[int, List[Dict[str, float | str]]]:
    model = pipe.named_steps.get("model")
    rows: List[Dict[str, float | str]] = []
    if hasattr(model, "coef_"):
        coefs = np.asarray(model.coef_)
        vals = np.max(np.abs(coefs), axis=0) if coefs.ndim == 2 else np.abs(coefs)
        for f, v in zip(feature_names, vals):
            if abs(float(v)) > 1e-9:
                rows.append({"feature": f, "importance": float(abs(v))})
    elif hasattr(model, "feature_importances_"):
        vals = np.asarray(model.feature_importances_)
        for f, v in zip(feature_names, vals):
            if float(v) > 0:
                rows.append({"feature": f, "importance": float(v)})
    rows = sorted(rows, key=lambda r: float(r["importance"]), reverse=True)
    return len(rows), rows[:50]


def evaluate_model(train: pd.DataFrame, test: pd.DataFrame, features: List[str], target: str, model_name: str, cfg: AntifragileConfig) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    y_train = train[target].astype(str)
    y_test = test[target].astype(str)
    classes = sorted(set(y_train) | set(y_test))
    if len(set(y_train)) < 2 or len(test) < 10:
        return {"target": target, "model": model_name, "status": "skipped_insufficient_classes_or_test"}, []
    X_train = train[features]
    X_test = test[features]
    pipe = make_pipeline(model_name, len(features), cfg)
    try:
        pipe.fit(X_train, y_train)
        pred_train = pipe.predict(X_train)
        pred_test = pipe.predict(X_test)
    except Exception as exc:
        return {"target": target, "model": model_name, "status": f"failed:{exc}"}, []

    base = baseline_score(y_train, y_test)
    train_bal = float(balanced_accuracy_score(y_train, pred_train))
    test_bal = float(balanced_accuracy_score(y_test, pred_test))
    test_acc = float(accuracy_score(y_test, pred_test))
    test_f1 = float(f1_score(y_test, pred_test, average="macro", zero_division=0))
    complexity, top = nonzero_complexity(pipe, features)
    gap = train_bal - test_bal
    baseline_bal = float(base.get("baseline_balanced_accuracy", np.nan))
    edge = test_bal - baseline_bal if not math.isnan(baseline_bal) else np.nan
    anti_score = test_bal - max(0.0, gap) - cfg.complexity_penalty_per_feature * min(complexity, 200)
    status = "accepted_challenger" if (edge >= cfg.min_edge_over_baseline and gap <= cfg.max_gap) else "rejected_by_antifragile_gate"
    if model_name == "neural_challenger":
        status = "neural_challenger_only" if edge >= cfg.min_edge_over_baseline and gap <= cfg.max_gap else "neural_rejected"
    result = {
        "target": target, "model": model_name, "status": status,
        "rows_train": int(len(train)), "rows_test": int(len(test)), "classes": ",".join(classes),
        "train_balanced_accuracy": train_bal,
        "test_balanced_accuracy": test_bal,
        "test_accuracy": test_acc,
        "test_macro_f1": test_f1,
        "baseline_label": base.get("baseline_label", ""),
        "baseline_accuracy": base.get("baseline_accuracy", np.nan),
        "baseline_balanced_accuracy": baseline_bal,
        "edge_over_baseline": edge,
        "train_test_gap": gap,
        "complexity_nonzero_features": int(complexity),
        "antifragile_score": anti_score,
    }
    for r in top:
        r["target"] = target
        r["model"] = model_name
    return result, top


def bin_series(s: pd.Series, train_idx: pd.Index) -> Tuple[pd.Series, Dict[str, float]]:
    x = pd.to_numeric(s, errors="coerce")
    tr = x.loc[train_idx].dropna()
    if len(tr) < 20 or tr.nunique() < 3:
        return pd.Series(["NA"] * len(s), index=s.index), {}
    q1, q2 = tr.quantile([0.33, 0.67]).values
    if not np.isfinite(q1) or not np.isfinite(q2) or abs(q2 - q1) < 1e-12:
        return pd.Series(["NA"] * len(s), index=s.index), {}
    b = pd.Series("MID", index=s.index)
    b[x <= q1] = "LOW"
    b[x >= q2] = "HIGH"
    b[x.isna()] = "NA"
    return b, {"q33": float(q1), "q67": float(q2)}


def positive_labels_for(target: str, values: Sequence[str]) -> List[str]:
    vals = sorted(set(str(v) for v in values))
    if "UP" in vals or "DOWN" in vals:
        return [v for v in ["UP", "DOWN"] if v in vals]
    return [v for v in vals if not (v.startswith("NO_") or v.startswith("NOT_") or v in {"FLAT", "0", "False", "false"})]


def mine_principles(df: pd.DataFrame, train: pd.DataFrame, test: pd.DataFrame, features: List[str], target: str, cfg: AntifragileConfig) -> pd.DataFrame:
    positives = positive_labels_for(target, df[target].dropna().astype(str).tolist())
    if not positives:
        return pd.DataFrame()
    rows: List[Dict[str, object]] = []
    train_idx, test_idx = train.index, test.index
    for f in features:
        bins, qs = bin_series(df[f], train_idx)
        if not qs:
            continue
        for state in ["LOW", "HIGH"]:
            mask_train = bins.loc[train_idx] == state
            mask_test = bins.loc[test_idx] == state
            if int(mask_train.sum()) < cfg.min_rule_support or int(mask_test.sum()) < cfg.min_oos_support:
                reason = "low_support"
            else:
                reason = ""
            for pos in positives:
                y_train = train[target].astype(str) == pos
                y_test = test[target].astype(str) == pos
                base_tr = float(y_train.mean()) if len(y_train) else np.nan
                base_te = float(y_test.mean()) if len(y_test) else np.nan
                cond_tr = float(y_train[mask_train].mean()) if mask_train.sum() else np.nan
                cond_te = float(y_test[mask_test].mean()) if mask_test.sum() else np.nan
                lift_tr = cond_tr / base_tr if base_tr and np.isfinite(base_tr) else np.nan
                lift_te = cond_te / base_te if base_te and np.isfinite(base_te) else np.nan
                gap = abs(lift_tr - lift_te) if np.isfinite(lift_tr) and np.isfinite(lift_te) else np.nan
                if reason == "":
                    if not np.isfinite(lift_tr) or lift_tr < cfg.min_lift:
                        reason = "weak_train_lift"
                    elif not np.isfinite(lift_te) or lift_te < cfg.min_lift:
                        reason = "no_oos_lift"
                    elif np.isfinite(gap) and gap > cfg.max_gap:
                        reason = "unstable_train_test_gap"
                    else:
                        reason = "accepted"
                family = f.split("__")[1] if f.startswith("concept__") and "__" in f else match_family(f)[0]
                rows.append({
                    "target": target,
                    "positive_label": pos,
                    "principle": f"{family}.{state} -> {pos}",
                    "feature": f,
                    "concept_family": family,
                    "state": state,
                    "train_support": int(mask_train.sum()),
                    "test_support": int(mask_test.sum()),
                    "train_event_rate": cond_tr,
                    "test_event_rate": cond_te,
                    "train_base_rate": base_tr,
                    "test_base_rate": base_te,
                    "train_lift": lift_tr,
                    "test_lift": lift_te,
                    "lift_gap": gap,
                    "verdict": reason,
                    "q33": qs.get("q33"), "q67": qs.get("q67"),
                })
    out = pd.DataFrame(rows)
    if not out.empty:
        out["principle_score"] = out["test_lift"].fillna(0) - out["lift_gap"].fillna(9) * 0.5 + np.log1p(out["test_support"].fillna(0)) * 0.02
        out = out.sort_values(["verdict", "principle_score"], ascending=[True, False])
    return out


def ablation_stability(model_results: pd.DataFrame, principles: pd.DataFrame) -> pd.DataFrame:
    if principles.empty:
        return pd.DataFrame()
    accepted = principles[principles["verdict"] == "accepted"].copy()
    if accepted.empty:
        return accepted
    grp = accepted.groupby(["target", "concept_family"]).agg(
        accepted_principles=("principle", "count"),
        mean_test_lift=("test_lift", "mean"),
        min_test_lift=("test_lift", "min"),
        max_lift_gap=("lift_gap", "max"),
        total_test_support=("test_support", "sum"),
    ).reset_index()
    grp["concept_verdict"] = np.where((grp["mean_test_lift"] >= 1.08) & (grp["max_lift_gap"] <= 0.14), "stable_concept", "fragile_concept")
    return grp.sort_values(["concept_verdict", "mean_test_lift", "total_test_support"], ascending=[True, False, False])


def write_markdown(out_dir: Path, cfg: AntifragileConfig, model_results: pd.DataFrame, principles: pd.DataFrame, concepts: pd.DataFrame) -> None:
    md: List[str] = []
    md.append("# Antifragile Astro Learning Report")
    md.append("")
    md.append("This report is intentionally skeptical. It prefers broad principles over brittle details, simple models over complex models, and out-of-sample survival over in-sample beauty.")
    md.append("")
    md.append("## Thinking contract")
    md.append("- Reduce first: collapse mechanical features into broad concept families.")
    md.append("- Think in alternatives: direction, clean path, spike, bull trap, bear trap can all be true/false independently.")
    md.append("- Do not worship neural nets: deep models are challengers only unless they survive OOS and explainability gates.")
    md.append("- Reject added conditions unless they improve OOS lift and reduce fragility.")
    md.append("- A principle is knowledge only if it has support, OOS lift, and small train/test gap.")
    md.append("")
    md.append("## Model gate summary")
    if model_results.empty:
        md.append("No model results were produced.")
    else:
        top = model_results.sort_values("antifragile_score", ascending=False).head(20)
        for _, r in top.iterrows():
            md.append(f"- `{r['target']}` / `{r['model']}`: status=`{r['status']}`, OOS balanced accuracy={r['test_balanced_accuracy']:.4f}, edge={r['edge_over_baseline']:.4f}, gap={r['train_test_gap']:.4f}, complexity={int(r['complexity_nonzero_features'])}")
    md.append("")
    md.append("## Accepted principles")
    acc = principles[principles["verdict"] == "accepted"].copy() if not principles.empty else pd.DataFrame()
    if acc.empty:
        md.append("No principle passed the antifragile gate. This is a valid result: the system refused to memorize fragile patterns.")
    else:
        for _, r in acc.sort_values("principle_score", ascending=False).head(40).iterrows():
            md.append(f"- `{r['principle']}` | target=`{r['target']}` | train_lift={r['train_lift']:.3f} | test_lift={r['test_lift']:.3f} | gap={r['lift_gap']:.3f} | test_support={int(r['test_support'])}")
    md.append("")
    md.append("## Stable concept families")
    if concepts.empty:
        md.append("No stable concepts extracted.")
    else:
        for _, r in concepts.head(30).iterrows():
            md.append(f"- `{r['concept_family']}` for `{r['target']}`: verdict={r['concept_verdict']}, accepted={int(r['accepted_principles'])}, mean_oos_lift={r['mean_test_lift']:.3f}, support={int(r['total_test_support'])}")
    md.append("")
    md.append("## How to use this knowledge")
    md.append("Use accepted principles as regime filters or warnings, not as standalone trade entries. If a model wins but no principle survives, treat it as a research lead, not production knowledge.")
    (out_dir / "ANTIFRAGILE_LEARNING_REPORT.md").write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build antifragile, principle-first astro learning memory from an EXP0016 dataset.")
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--targets", default="")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--test-fraction", type=float, default=0.25)
    ap.add_argument("--min-rule-support", type=int, default=120)
    ap.add_argument("--min-oos-support", type=int, default=40)
    ap.add_argument("--min-lift", type=float, default=1.08)
    ap.add_argument("--max-gap", type=float, default=0.14)
    ap.add_argument("--enable-neural-challenger", action="store_true")
    ap.add_argument("--neural-min-rows", type=int, default=8000)
    args = ap.parse_args()

    cfg = AntifragileConfig(test_fraction=args.test_fraction, min_rule_support=args.min_rule_support, min_oos_support=args.min_oos_support, min_lift=args.min_lift, max_gap=args.max_gap, neural_min_rows=args.neural_min_rows)
    common = Path(args.common_files)
    run_id = f"{now_id()}_{stable_run_id([args.asset, args.timeframe, args.dataset_csv, 'antifragile'])}"
    out_dir = Path(args.out_dir) if args.out_dir else common / "astro_ml" / "antifragile_memory" / args.asset.upper() / args.timeframe.upper() / run_id
    ensure_dir(out_dir)

    df = read_csv_flexible(args.dataset_csv)
    try:
        df, time_col = normalize_time_column(df)
    except Exception:
        time_col = ""
    raw_cols = numeric_feature_columns(df)
    concept_df, mapping = build_concept_frame(df, raw_cols)
    targets = target_columns(df, args.targets)
    if not targets:
        raise SystemExit("No target columns found. Expected label_* columns in dataset.")

    # concept-first features + a small raw residual set. This is the reduction principle.
    concept_features = list(concept_df.columns)[:cfg.max_concept_features]
    raw_kept = raw_cols[:cfg.max_raw_features]
    work = pd.concat([df.reset_index(drop=True), concept_df.reset_index(drop=True)], axis=1)

    model_rows: List[Dict[str, object]] = []
    importance_rows: List[Dict[str, object]] = []
    principle_frames: List[pd.DataFrame] = []
    feature_sets = {
        "concept_only": concept_features,
        "concept_plus_small_raw": concept_features + raw_kept,
    }
    base_models = ["occam_l1_logistic", "shallow_tree", "small_forest", "extra_trees_challenger"]
    if args.enable_neural_challenger and len(work) >= cfg.neural_min_rows:
        base_models.append("neural_challenger")

    for target in targets:
        train, test = chronological_split(work, target, cfg.test_fraction)
        if len(train) < cfg.min_train_rows and len(work) > cfg.min_train_rows:
            # If short dataset, still run but mark rows. If very tiny, scripts will skip.
            pass
        for fs_name, feats in feature_sets.items():
            feats = [f for f in feats if f in work.columns]
            if not feats:
                continue
            for model_name in base_models:
                result, top = evaluate_model(train, test, feats, target, model_name, cfg)
                result["feature_set"] = fs_name
                model_rows.append(result)
                for r in top:
                    r["feature_set"] = fs_name
                    importance_rows.append(r)
        # principle mining is concept-only by design: knowledge should be simple.
        principle_frames.append(mine_principles(work, train, test, concept_features, target, cfg))

    model_results = pd.DataFrame(model_rows)
    importances = pd.DataFrame(importance_rows)
    principles = pd.concat([p for p in principle_frames if p is not None and not p.empty], ignore_index=True) if principle_frames else pd.DataFrame()
    concepts = ablation_stability(model_results, principles)

    mapping.to_csv(out_dir / "feature_to_concept_map.csv", index=False)
    concept_df.to_csv(out_dir / "concept_abstraction_dataset.csv", index=False)
    model_results.to_csv(out_dir / "antifragile_model_gate.csv", index=False)
    importances.to_csv(out_dir / "antifragile_importance.csv", index=False)
    principles.to_csv(out_dir / "antifragile_principles.csv", index=False)
    concepts.to_csv(out_dir / "stable_concepts.csv", index=False)

    # Portable mind state.
    mind = {
        "asset": args.asset.upper(), "timeframe": args.timeframe.upper(), "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_csv": args.dataset_csv,
        "config": asdict(cfg),
        "targets": targets,
        "doctrine": "antifragile_reductive_skeptical_principle_first",
        "accepted_principles": principles[principles["verdict"] == "accepted"].sort_values("principle_score", ascending=False).head(100).to_dict("records") if not principles.empty else [],
        "stable_concepts": concepts.head(100).to_dict("records") if not concepts.empty else [],
        "best_models": model_results.sort_values("antifragile_score", ascending=False).head(50).to_dict("records") if not model_results.empty and "antifragile_score" in model_results else [],
    }
    save_json(out_dir / "antifragile_mind.json", mind)

    try:
        with pd.ExcelWriter(out_dir / "antifragile_learning_report.xlsx", engine="openpyxl") as writer:
            model_results.to_excel(writer, sheet_name="ModelGate", index=False)
            principles.to_excel(writer, sheet_name="Principles", index=False)
            concepts.to_excel(writer, sheet_name="StableConcepts", index=False)
            importances.to_excel(writer, sheet_name="Importance", index=False)
            mapping.to_excel(writer, sheet_name="FeatureConceptMap", index=False)
    except Exception as exc:
        (out_dir / "excel_error.txt").write_text(str(exc), encoding="utf-8")

    write_markdown(out_dir, cfg, model_results, principles, concepts)
    print(f"ANTIFRAGILE_MEMORY_DIR={out_dir}")
    print(f"ANTIFRAGILE_REPORT={out_dir / 'ANTIFRAGILE_LEARNING_REPORT.md'}")
    print(f"ANTIFRAGILE_MIND={out_dir / 'antifragile_mind.json'}")
    print(f"ANTIFRAGILE_ACCEPTED_PRINCIPLES={0 if principles.empty else int((principles['verdict']=='accepted').sum())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
