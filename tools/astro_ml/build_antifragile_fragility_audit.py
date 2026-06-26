#!/usr/bin/env python3
"""
EXP0016 - Antifragile Fragility Audit.

This module audits the *thinking* of the antifragile learner rather than merely
retraining another model. It searches for the places where a learned astro logic
can become fragile:

- temporal single-split overfit
- regime/subperiod instability
- one-concept monoculture dependency
- perturbation sensitivity
- contradictory multi-target interpretation
- condition creep / rule proliferation
- weak support disguised as insight

The output is a hardened mind: accepted principles must survive time folds,
small input perturbations, and parsimony gates before they are promoted from
"interesting pattern" to "usable knowledge".
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

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, normalize_time_column, read_csv_flexible, save_json, stable_run_id
from build_antifragile_astro_learning import (
    AntifragileConfig,
    build_concept_frame,
    chronological_split,
    make_pipeline,
    numeric_feature_columns,
    target_columns,
    positive_labels_for,
)

from sklearn.metrics import balanced_accuracy_score, accuracy_score, f1_score


@dataclass
class FragilityAuditConfig:
    folds: int = 6
    min_fold_support: int = 25
    min_survival_rate: float = 0.60
    min_median_lift: float = 1.05
    min_worst_lift: float = 0.95
    max_lift_iqr: float = 0.65
    test_fraction: float = 0.25
    perturb_repeats: int = 24
    perturb_noise_scale: float = 0.035
    perturb_dropout_rate: float = 0.10
    max_perturb_bal_acc_drop: float = 0.055
    max_single_concept_dependency_drop: float = 0.12
    max_rules_per_target: int = 12
    max_rules_per_concept_target: int = 4
    min_oos_edge_over_baseline: float = 0.015
    random_state: int = 42


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def discover_antifragile_dir(common: Path, asset: str, timeframe: str, provided: str = "") -> Optional[Path]:
    if provided:
        p = Path(provided)
        if not p.is_absolute():
            p = common / p
        return p if p.exists() else None
    root = common / "astro_ml" / "antifragile_memory" / asset.upper() / timeframe.upper()
    if not root.exists():
        return None
    dirs = [p for p in root.iterdir() if p.is_dir()]
    if not dirs:
        return None
    return sorted(dirs, key=lambda x: x.stat().st_mtime, reverse=True)[0]


def split_folds(n: int, k: int) -> List[Tuple[int, int]]:
    k = max(2, min(k, max(2, n // 50))) if n >= 100 else max(2, min(k, n))
    idx = np.array_split(np.arange(n), k)
    out: List[Tuple[int, int]] = []
    for a in idx:
        if len(a):
            out.append((int(a[0]), int(a[-1]) + 1))
    return out


def state_mask_from_threshold(x: pd.Series, state: str, q33: float, q67: float) -> pd.Series:
    vals = pd.to_numeric(x, errors="coerce")
    if state == "LOW":
        return vals <= q33
    if state == "HIGH":
        return vals >= q67
    if state == "MID":
        return (vals > q33) & (vals < q67)
    return pd.Series(False, index=x.index)


def load_principles(anti_dir: Optional[Path]) -> pd.DataFrame:
    if anti_dir is None:
        return pd.DataFrame()
    p = anti_dir / "antifragile_principles.csv"
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()


def accepted_or_candidate_principles(principles: pd.DataFrame) -> pd.DataFrame:
    if principles.empty:
        return pd.DataFrame()
    if "verdict" not in principles.columns:
        return principles.copy()
    acc = principles[principles["verdict"].astype(str).str.lower().eq("accepted")].copy()
    if len(acc) >= 1:
        return acc
    # If nothing survived the previous layer, audit the strongest rejected rules too.
    score_col = "principle_score" if "principle_score" in principles.columns else None
    if score_col:
        return principles.sort_values(score_col, ascending=False).head(100).copy()
    return principles.head(100).copy()


def temporal_principle_stress(work: pd.DataFrame, principles: pd.DataFrame, cfg: FragilityAuditConfig) -> pd.DataFrame:
    cand = accepted_or_candidate_principles(principles)
    if cand.empty:
        return pd.DataFrame()
    folds = split_folds(len(work), cfg.folds)
    rows: List[Dict[str, object]] = []
    for _, r in cand.iterrows():
        target = str(r.get("target", ""))
        feature = str(r.get("feature", ""))
        state = str(r.get("state", ""))
        pos = str(r.get("positive_label", ""))
        if not target or target not in work.columns or feature not in work.columns or not pos:
            continue
        try:
            q33 = float(r.get("q33"))
            q67 = float(r.get("q67"))
        except Exception:
            vals = pd.to_numeric(work[feature], errors="coerce").dropna()
            if len(vals) < 20:
                continue
            q33, q67 = vals.quantile([0.33, 0.67]).values
        mask = state_mask_from_threshold(work[feature], state, q33, q67)
        lifts: List[float] = []
        supports: List[int] = []
        fold_rows: List[Dict[str, object]] = []
        for fold_id, (a, b) in enumerate(folds, start=1):
            d = work.iloc[a:b]
            m = mask.iloc[a:b]
            y = d[target].astype(str).eq(pos)
            support = int(m.sum())
            base = float(y.mean()) if len(y) else np.nan
            cond = float(y[m].mean()) if support else np.nan
            lift = cond / base if base and np.isfinite(base) else np.nan
            lifts.append(float(lift) if np.isfinite(lift) else np.nan)
            supports.append(support)
            fold_rows.append({
                "fold": fold_id,
                "support": support,
                "base_rate": base,
                "event_rate": cond,
                "lift": lift,
            })
        finite = np.array([x for x in lifts if np.isfinite(x)], dtype=float)
        support_ok = np.array([s >= cfg.min_fold_support for s in supports])
        survive = np.array([(np.isfinite(l) and l >= 1.0 and s >= cfg.min_fold_support) for l, s in zip(lifts, supports)])
        survival_rate = float(survive.mean()) if len(survive) else 0.0
        median_lift = float(np.nanmedian(finite)) if len(finite) else np.nan
        worst_lift = float(np.nanmin(finite)) if len(finite) else np.nan
        lift_iqr = float(np.nanpercentile(finite, 75) - np.nanpercentile(finite, 25)) if len(finite) >= 3 else np.nan
        verdict = "hardened"
        reasons: List[str] = []
        if survival_rate < cfg.min_survival_rate:
            verdict = "fragile"; reasons.append("low_temporal_survival")
        if not np.isfinite(median_lift) or median_lift < cfg.min_median_lift:
            verdict = "fragile"; reasons.append("weak_median_lift")
        if not np.isfinite(worst_lift) or worst_lift < cfg.min_worst_lift:
            verdict = "fragile"; reasons.append("bad_worst_fold")
        if np.isfinite(lift_iqr) and lift_iqr > cfg.max_lift_iqr:
            verdict = "fragile"; reasons.append("unstable_lift_iqr")
        if sum(support_ok) < max(2, int(math.ceil(cfg.min_survival_rate * len(folds)))):
            verdict = "fragile"; reasons.append("thin_support_across_time")
        rows.append({
            "target": target,
            "positive_label": pos,
            "principle": r.get("principle", f"{feature}.{state}->{pos}"),
            "feature": feature,
            "concept_family": r.get("concept_family", concept_from_feature(feature)),
            "state": state,
            "folds": len(folds),
            "survival_rate": survival_rate,
            "median_lift": median_lift,
            "worst_lift": worst_lift,
            "lift_iqr": lift_iqr,
            "min_fold_support": int(min(supports)) if supports else 0,
            "median_fold_support": float(np.median(supports)) if supports else 0.0,
            "temporal_verdict": verdict,
            "fragility_reason": ";".join(reasons) if reasons else "survived_temporal_stress",
            "fold_detail_json": json.dumps(fold_rows),
        })
    out = pd.DataFrame(rows)
    if not out.empty:
        out["temporal_score"] = out["median_lift"].fillna(0) - out["lift_iqr"].fillna(9) * 0.25 + out["survival_rate"].fillna(0) * 0.25
        out = out.sort_values(["temporal_verdict", "temporal_score"], ascending=[True, False])
    return out


def concept_from_feature(f: str) -> str:
    s = str(f)
    if s.startswith("concept__") and "__" in s:
        parts = s.split("__")
        if len(parts) >= 3:
            return parts[1]
    return "raw_or_misc"


def concept_groups(features: List[str]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for f in features:
        groups.setdefault(concept_from_feature(f), []).append(f)
    return groups


def get_xy(train: pd.DataFrame, test: pd.DataFrame, features: List[str], target: str):
    y_train = train[target].astype(str)
    y_test = test[target].astype(str)
    return train[features], test[features], y_train, y_test


def train_eval_model(train: pd.DataFrame, test: pd.DataFrame, features: List[str], target: str, model_name: str, seed: int) -> Tuple[Optional[object], Dict[str, object]]:
    if len(features) < 1 or target not in train.columns or len(set(train[target].astype(str))) < 2 or len(test) < 20:
        return None, {"status": "skipped"}
    cfg = AntifragileConfig(random_state=seed)
    pipe = make_pipeline(model_name, len(features), cfg)
    X_train, X_test, y_train, y_test = get_xy(train, test, features, target)
    try:
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        train_pred = pipe.predict(X_train)
    except Exception as exc:
        return None, {"status": f"failed:{exc}"}
    return pipe, {
        "status": "ok",
        "test_balanced_accuracy": float(balanced_accuracy_score(y_test, pred)),
        "train_balanced_accuracy": float(balanced_accuracy_score(y_train, train_pred)),
        "test_accuracy": float(accuracy_score(y_test, pred)),
        "test_macro_f1": float(f1_score(y_test, pred, average="macro", zero_division=0)),
        "train_test_gap": float(balanced_accuracy_score(y_train, train_pred) - balanced_accuracy_score(y_test, pred)),
    }


def perturbation_stress(work: pd.DataFrame, targets: List[str], features: List[str], cfg: FragilityAuditConfig) -> pd.DataFrame:
    if not features:
        return pd.DataFrame()
    rng = np.random.default_rng(cfg.random_state)
    rows: List[Dict[str, object]] = []
    groups = concept_groups(features)
    for target in targets:
        train, test = chronological_split(work, target, cfg.test_fraction)
        if len(train) < 100 or len(test) < 20 or len(set(train[target].dropna().astype(str))) < 2:
            continue
        for model_name in ["occam_l1_logistic", "shallow_tree", "small_forest"]:
            pipe, base = train_eval_model(train, test, features, target, model_name, cfg.random_state)
            if pipe is None or base.get("status") != "ok":
                continue
            y_test = test[target].astype(str)
            original = float(base["test_balanced_accuracy"])
            med = train[features].median(numeric_only=True)
            std = train[features].std(numeric_only=True).replace(0, np.nan).fillna(1.0)
            noise_scores: List[float] = []
            dropout_scores: List[float] = []
            for _ in range(cfg.perturb_repeats):
                xt = test[features].copy()
                noise = rng.normal(0.0, cfg.perturb_noise_scale, size=xt.shape)
                xt_noise = xt + noise * std.values.reshape(1, -1)
                try:
                    noise_scores.append(float(balanced_accuracy_score(y_test, pipe.predict(xt_noise))))
                except Exception:
                    pass
                xt_drop = xt.copy()
                n_drop = max(1, int(len(features) * cfg.perturb_dropout_rate))
                drop_cols = rng.choice(features, size=min(n_drop, len(features)), replace=False)
                for c in drop_cols:
                    xt_drop[c] = med.get(c, 0.0)
                try:
                    dropout_scores.append(float(balanced_accuracy_score(y_test, pipe.predict(xt_drop))))
                except Exception:
                    pass
            noise_mean = float(np.mean(noise_scores)) if noise_scores else np.nan
            drop_mean = float(np.mean(dropout_scores)) if dropout_scores else np.nan
            worst_drop = original - min([x for x in [noise_mean, drop_mean] if np.isfinite(x)] or [original])
            verdict = "robust" if worst_drop <= cfg.max_perturb_bal_acc_drop else "fragile"
            rows.append({
                "target": target,
                "model": model_name,
                "original_balanced_accuracy": original,
                "noise_mean_balanced_accuracy": noise_mean,
                "feature_dropout_mean_balanced_accuracy": drop_mean,
                "max_perturbation_drop": worst_drop,
                "perturbation_verdict": verdict,
            })
    return pd.DataFrame(rows)


def concept_dependency_stress(work: pd.DataFrame, targets: List[str], features: List[str], cfg: FragilityAuditConfig) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    groups = concept_groups(features)
    for target in targets:
        train, test = chronological_split(work, target, cfg.test_fraction)
        if len(train) < 100 or len(test) < 20 or len(set(train[target].dropna().astype(str))) < 2:
            continue
        pipe, base = train_eval_model(train, test, features, target, "small_forest", cfg.random_state)
        if pipe is None or base.get("status") != "ok":
            continue
        base_score = float(base["test_balanced_accuracy"])
        for concept, cols in groups.items():
            kept = [f for f in features if f not in cols]
            if not kept:
                continue
            _, res = train_eval_model(train, test, kept, target, "small_forest", cfg.random_state)
            if res.get("status") != "ok":
                continue
            score = float(res["test_balanced_accuracy"])
            drop = base_score - score
            if drop > cfg.max_single_concept_dependency_drop:
                verdict = "monoculture_dependency_risk"
            elif drop < -0.02:
                verdict = "concept_may_be_noise"
            else:
                verdict = "distributed_dependency"
            rows.append({
                "target": target,
                "concept_family_removed": concept,
                "removed_features": len(cols),
                "base_balanced_accuracy": base_score,
                "without_concept_balanced_accuracy": score,
                "dependency_drop": drop,
                "dependency_verdict": verdict,
            })
    return pd.DataFrame(rows).sort_values(["target", "dependency_drop"], ascending=[True, False]) if rows else pd.DataFrame()


def contradiction_audit(principles: pd.DataFrame) -> pd.DataFrame:
    if principles.empty:
        return pd.DataFrame()
    p = accepted_or_candidate_principles(principles)
    if p.empty:
        return pd.DataFrame()
    rows: List[Dict[str, object]] = []
    # Direction contradictions: same concept/state/horizon supports both UP and DOWN.
    p = p.copy()
    p["horizon"] = p["target"].astype(str).str.extract(r"_(\d+)$", expand=False).fillna("")
    key_cols = ["concept_family", "state", "horizon"]
    for key, g in p.groupby(key_cols, dropna=False):
        labels = sorted(set(g.get("positive_label", pd.Series(dtype=str)).astype(str)))
        targets = sorted(set(g.get("target", pd.Series(dtype=str)).astype(str)))
        if "UP" in labels and "DOWN" in labels:
            rows.append({
                "fragility_type": "directional_contradiction",
                "key": str(key),
                "labels": ",".join(labels),
                "targets": ",".join(targets),
                "reason": "same broad concept/state supports both UP and DOWN on the same horizon",
            })
        # Clean long + clean short contradiction under same concept/state/horizon.
        if any("CLEAN_LONG" in x for x in labels) and any("CLEAN_SHORT" in x for x in labels):
            rows.append({
                "fragility_type": "path_side_contradiction",
                "key": str(key),
                "labels": ",".join(labels),
                "targets": ",".join(targets),
                "reason": "same concept/state supports both clean long and clean short",
            })
    return pd.DataFrame(rows)


def condition_creep_audit(principles: pd.DataFrame, cfg: FragilityAuditConfig) -> pd.DataFrame:
    if principles.empty:
        return pd.DataFrame()
    p = accepted_or_candidate_principles(principles)
    if p.empty:
        return pd.DataFrame()
    rows: List[Dict[str, object]] = []
    by_target = p.groupby("target").size()
    for target, n in by_target.items():
        if int(n) > cfg.max_rules_per_target:
            rows.append({
                "fragility_type": "condition_creep_target",
                "target": target,
                "count": int(n),
                "limit": cfg.max_rules_per_target,
                "reason": "too many accepted/candidate principles for one target; likely rule proliferation",
            })
    if all(c in p.columns for c in ["target", "concept_family"]):
        for (target, concept), n in p.groupby(["target", "concept_family"]).size().items():
            if int(n) > cfg.max_rules_per_concept_target:
                rows.append({
                    "fragility_type": "condition_creep_concept",
                    "target": target,
                    "concept_family": concept,
                    "count": int(n),
                    "limit": cfg.max_rules_per_concept_target,
                    "reason": "too many principles from the same concept for one target; compress or reject details",
                })
    return pd.DataFrame(rows)


def build_hardened_principles(principles: pd.DataFrame, temporal: pd.DataFrame, contradictions: pd.DataFrame, creep: pd.DataFrame) -> pd.DataFrame:
    if principles.empty or temporal.empty:
        return pd.DataFrame()
    p = accepted_or_candidate_principles(principles).copy()
    key_cols = ["target", "positive_label", "feature", "state"]
    for c in key_cols:
        if c not in p.columns or c not in temporal.columns:
            return pd.DataFrame()
    merged = p.merge(temporal[key_cols + ["temporal_verdict", "fragility_reason", "survival_rate", "median_lift", "worst_lift", "lift_iqr", "temporal_score"]], on=key_cols, how="left")
    merged["hardened_verdict"] = np.where(merged["temporal_verdict"].eq("hardened"), "hardened", "rejected_by_fragility_audit")
    merged["hardening_reason"] = np.where(merged["hardened_verdict"].eq("hardened"), "survived_temporal_fragility_audit", merged["fragility_reason"].fillna("not_stressed"))
    return merged.sort_values(["hardened_verdict", "temporal_score"], ascending=[True, False])


def write_markdown(out_dir: Path, cfg: FragilityAuditConfig, temporal: pd.DataFrame, perturb: pd.DataFrame, dependency: pd.DataFrame, contradictions: pd.DataFrame, creep: pd.DataFrame, hardened: pd.DataFrame) -> None:
    md: List[str] = []
    md.append("# Antifragile Fragility Audit Report")
    md.append("")
    md.append("This layer audits the failure modes of the learner's thinking. It assumes that the model is guilty until it survives time, perturbation, dependency, contradiction, and parsimony stress tests.")
    md.append("")
    md.append("## Fragility assumptions tested")
    md.append("- A single chronological split may be lucky.")
    md.append("- A rule can look strong in aggregate while failing in most subperiods.")
    md.append("- A model can depend on one concept family and become a monoculture.")
    md.append("- A model can be sensitive to small numeric perturbations.")
    md.append("- A concept can support contradictory interpretations across targets.")
    md.append("- Too many accepted rules usually means condition creep, not intelligence.")
    md.append("")
    md.append("## Hardened principles")
    if hardened.empty:
        md.append("No principle was hardened. This is acceptable: the learner refused to promote fragile patterns.")
    else:
        h = hardened[hardened["hardened_verdict"].eq("hardened")]
        if h.empty:
            md.append("No principle survived the hardening gate.")
        else:
            for _, r in h.head(40).iterrows():
                md.append(f"- `{r.get('principle')}` | target=`{r.get('target')}` | survival={float(r.get('survival_rate', np.nan)):.2f} | median_lift={float(r.get('median_lift', np.nan)):.3f} | worst_lift={float(r.get('worst_lift', np.nan)):.3f}")
    md.append("")
    md.append("## Model perturbation stress")
    if perturb.empty:
        md.append("No perturbation stress was produced.")
    else:
        for _, r in perturb.sort_values("max_perturbation_drop", ascending=False).head(20).iterrows():
            md.append(f"- `{r['target']}` / `{r['model']}`: verdict=`{r['perturbation_verdict']}`, original={r['original_balanced_accuracy']:.4f}, max_drop={r['max_perturbation_drop']:.4f}")
    md.append("")
    md.append("## Concept dependency stress")
    if dependency.empty:
        md.append("No concept dependency stress was produced.")
    else:
        for _, r in dependency.sort_values("dependency_drop", ascending=False).head(20).iterrows():
            md.append(f"- `{r['target']}` loses `{r['dependency_drop']:.4f}` balanced accuracy when `{r['concept_family_removed']}` is removed: `{r['dependency_verdict']}`")
    md.append("")
    md.append("## Contradiction and condition-creep flags")
    if contradictions.empty and creep.empty:
        md.append("No contradiction or condition-creep flags were found.")
    else:
        if not contradictions.empty:
            for _, r in contradictions.head(20).iterrows():
                md.append(f"- contradiction `{r['fragility_type']}`: {r['reason']} | key={r['key']}")
        if not creep.empty:
            for _, r in creep.head(20).iterrows():
                md.append(f"- condition creep `{r['fragility_type']}`: {r['reason']}")
    md.append("")
    md.append("## Operational rule")
    md.append("Only hardened principles can be promoted to reusable knowledge. Non-hardened patterns may remain in research memory, but they must not become production filters or MQL rules.")
    (out_dir / "FRAGILITY_AUDIT_REPORT.md").write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit and harden EXP0016 antifragile astro memory against temporal, perturbation, dependency, contradiction, and condition-creep fragility.")
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--antifragile-dir", default="")
    ap.add_argument("--targets", default="")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--folds", type=int, default=6)
    ap.add_argument("--min-fold-support", type=int, default=25)
    ap.add_argument("--min-survival-rate", type=float, default=0.60)
    ap.add_argument("--min-median-lift", type=float, default=1.05)
    ap.add_argument("--min-worst-lift", type=float, default=0.95)
    ap.add_argument("--max-lift-iqr", type=float, default=0.65)
    ap.add_argument("--perturb-repeats", type=int, default=24)
    ap.add_argument("--perturb-noise-scale", type=float, default=0.035)
    ap.add_argument("--perturb-dropout-rate", type=float, default=0.10)
    ap.add_argument("--max-perturb-drop", type=float, default=0.055)
    ap.add_argument("--max-concept-dependency-drop", type=float, default=0.12)
    ap.add_argument("--max-rules-per-target", type=int, default=12)
    ap.add_argument("--max-rules-per-concept-target", type=int, default=4)
    args = ap.parse_args()

    cfg = FragilityAuditConfig(
        folds=args.folds,
        min_fold_support=args.min_fold_support,
        min_survival_rate=args.min_survival_rate,
        min_median_lift=args.min_median_lift,
        min_worst_lift=args.min_worst_lift,
        max_lift_iqr=args.max_lift_iqr,
        perturb_repeats=args.perturb_repeats,
        perturb_noise_scale=args.perturb_noise_scale,
        perturb_dropout_rate=args.perturb_dropout_rate,
        max_perturb_bal_acc_drop=args.max_perturb_drop,
        max_single_concept_dependency_drop=args.max_concept_dependency_drop,
        max_rules_per_target=args.max_rules_per_target,
        max_rules_per_concept_target=args.max_rules_per_concept_target,
    )
    common = Path(args.common_files)
    run_id = f"{now_id()}_{stable_run_id([args.asset, args.timeframe, args.dataset_csv, 'fragility_audit'])}"
    out_dir = Path(args.out_dir) if args.out_dir else common / "astro_ml" / "antifragile_fragility_audits" / args.asset.upper() / args.timeframe.upper() / run_id
    ensure_dir(out_dir)

    df = read_csv_flexible(args.dataset_csv)
    try:
        df, time_col = normalize_time_column(df)
    except Exception:
        time_col = ""
    raw_cols = numeric_feature_columns(df)
    concept_df, mapping = build_concept_frame(df, raw_cols)
    work = pd.concat([df.reset_index(drop=True), concept_df.reset_index(drop=True)], axis=1)
    concept_features = list(concept_df.columns)
    targets = target_columns(work, args.targets)
    if not targets:
        raise SystemExit("No label targets found for fragility audit.")

    anti_dir = discover_antifragile_dir(common, args.asset, args.timeframe, args.antifragile_dir)
    principles = load_principles(anti_dir)

    temporal = temporal_principle_stress(work, principles, cfg)
    perturb = perturbation_stress(work, targets, concept_features, cfg)
    dependency = concept_dependency_stress(work, targets, concept_features, cfg)
    contradictions = contradiction_audit(principles)
    creep = condition_creep_audit(principles, cfg)
    hardened = build_hardened_principles(principles, temporal, contradictions, creep)

    temporal.to_csv(out_dir / "temporal_principle_stress.csv", index=False)
    perturb.to_csv(out_dir / "perturbation_stress.csv", index=False)
    dependency.to_csv(out_dir / "concept_dependency_stress.csv", index=False)
    contradictions.to_csv(out_dir / "contradiction_flags.csv", index=False)
    creep.to_csv(out_dir / "condition_creep_flags.csv", index=False)
    hardened.to_csv(out_dir / "hardened_principles.csv", index=False)
    mapping.to_csv(out_dir / "feature_to_concept_map.csv", index=False)

    flags: List[Dict[str, object]] = []
    if not temporal.empty:
        for _, r in temporal[temporal["temporal_verdict"].eq("fragile")].head(200).iterrows():
            flags.append({"source": "temporal", "target": r.get("target"), "item": r.get("principle"), "reason": r.get("fragility_reason")})
    if not perturb.empty:
        for _, r in perturb[perturb["perturbation_verdict"].eq("fragile")].head(100).iterrows():
            flags.append({"source": "perturbation", "target": r.get("target"), "item": r.get("model"), "reason": f"max_drop={r.get('max_perturbation_drop')}"})
    if not dependency.empty:
        for _, r in dependency[dependency["dependency_verdict"].eq("monoculture_dependency_risk")].head(100).iterrows():
            flags.append({"source": "dependency", "target": r.get("target"), "item": r.get("concept_family_removed"), "reason": f"dependency_drop={r.get('dependency_drop')}"})
    if not contradictions.empty:
        for _, r in contradictions.head(100).iterrows():
            flags.append({"source": "contradiction", "target": "", "item": r.get("key"), "reason": r.get("reason")})
    if not creep.empty:
        for _, r in creep.head(100).iterrows():
            flags.append({"source": "condition_creep", "target": r.get("target", ""), "item": r.get("concept_family", ""), "reason": r.get("reason")})
    flags_df = pd.DataFrame(flags)
    flags_df.to_csv(out_dir / "fragility_flags.csv", index=False)

    hardened_count = int((hardened["hardened_verdict"] == "hardened").sum()) if not hardened.empty and "hardened_verdict" in hardened.columns else 0
    decision_memory = {
        "asset": args.asset.upper(),
        "timeframe": args.timeframe.upper(),
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_csv": args.dataset_csv,
        "antifragile_dir": str(anti_dir) if anti_dir else "",
        "config": asdict(cfg),
        "targets": targets,
        "hardened_principles_count": hardened_count,
        "fragility_flags_count": int(len(flags_df)),
        "thinking_patch": "use_hardened_principles_only; treat all fragile patterns as research leads; prefer concept families with temporal survival and low perturbation sensitivity",
        "hardened_principles": hardened[hardened["hardened_verdict"].eq("hardened")].head(100).to_dict("records") if hardened_count else [],
        "fragility_flags": flags_df.head(300).to_dict("records") if not flags_df.empty else [],
    }
    save_json(out_dir / "antifragile_decision_memory.json", decision_memory)

    try:
        with pd.ExcelWriter(out_dir / "fragility_audit_report.xlsx", engine="openpyxl") as writer:
            temporal.to_excel(writer, sheet_name="TemporalPrinciples", index=False)
            perturb.to_excel(writer, sheet_name="PerturbationStress", index=False)
            dependency.to_excel(writer, sheet_name="ConceptDependency", index=False)
            hardened.to_excel(writer, sheet_name="HardenedPrinciples", index=False)
            flags_df.to_excel(writer, sheet_name="FragilityFlags", index=False)
            contradictions.to_excel(writer, sheet_name="Contradictions", index=False)
            creep.to_excel(writer, sheet_name="ConditionCreep", index=False)
    except Exception as exc:
        (out_dir / "excel_error.txt").write_text(str(exc), encoding="utf-8")

    write_markdown(out_dir, cfg, temporal, perturb, dependency, contradictions, creep, hardened)
    print(f"FRAGILITY_AUDIT_DIR={out_dir}")
    print(f"FRAGILITY_AUDIT_REPORT={out_dir / 'FRAGILITY_AUDIT_REPORT.md'}")
    print(f"FRAGILITY_DECISION_MEMORY={out_dir / 'antifragile_decision_memory.json'}")
    print(f"HARDENED_PRINCIPLES={hardened_count}")
    print(f"FRAGILITY_FLAGS={len(flags_df)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
