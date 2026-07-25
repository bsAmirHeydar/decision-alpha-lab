#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, normalize_time_column, read_csv_flexible, save_excel, save_json

FAMILY_KEYWORDS = {
    "saturn_pressure": ["saturn", "constraint", "resistance"],
    "mars_impulse": ["mars", "impulse", "friction"],
    "jupiter_expansion": ["jupiter", "expansion", "support"],
    "venus_value": ["venus", "value", "benefic"],
    "moon_timing": ["moon", "lunar"],
    "mercury_information": ["mercury"],
    "pluto_pressure": ["pluto"],
    "natal_activation": ["natal"],
    "path_quality": ["path", "clean", "friction", "exhaust"],
    "macro_context": ["macro", "direction", "bias"],
    "timing": ["minute", "timing", "trigger", "phase"],
}

TEXT_CONTEXT_COLS = [
    "astro_language", "feature_key", "astro_signal_text", "astro_bias_text", "astro_path_text", "macro_context",
    "moon_phase_bucket", "moon_phase_half", "sect_name", "solar_quarter_name", "natal_label",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def infer_time_col(df: pd.DataFrame) -> str:
    d, tc = normalize_time_column(df)
    return tc


def candidate_features(df: pd.DataFrame, max_features: int = 80) -> List[str]:
    banned_prefix = ("label_", "ret_", "future_", "mfe_", "mae_", "clean_", "spike_", "trap_", "target_", "outcome_")
    banned_exact = {"open", "high", "low", "close", "time", "datetime", "broker_time", "utc_time", "tick_volume", "volume", "spread", "real_volume"}
    cols = []
    # First pass: prefer explicitly meaningful astro/score/natal/path columns.
    for c in df.columns:
        cl = str(c).lower()
        if c in banned_exact or any(cl.startswith(p) for p in banned_prefix):
            continue
        if pd.api.types.is_numeric_dtype(df[c]):
            if df[c].nunique(dropna=True) <= 1:
                continue
            score = 0
            for fam, keys in FAMILY_KEYWORDS.items():
                if any(k in cl for k in keys):
                    score += 10
            if "score" in cl or "bias" in cl or "pressure" in cl or "flow" in cl:
                score += 4
            if score > 0:
                cols.append((score, c))
    cols = [c for _, c in sorted(cols, key=lambda x: (-x[0], str(x[1])))[:max_features]]
    if len(cols) < 20:
        for c in df.columns:
            if c in cols:
                continue
            cl = str(c).lower()
            if c in banned_exact or any(cl.startswith(p) for p in banned_prefix):
                continue
            if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique(dropna=True) > 2:
                cols.append(c)
            if len(cols) >= max_features:
                break
    return cols


def bucket_series(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    if x.dropna().nunique() <= 2:
        return x.fillna(-999).astype(str)
    qs = x.quantile([0.1, 0.33, 0.66, 0.9]).to_dict()
    q10, q33, q66, q90 = qs.get(0.1), qs.get(0.33), qs.get(0.66), qs.get(0.9)
    def b(v):
        if pd.isna(v): return "missing"
        if q10 is not None and v <= q10: return "very_low"
        if q33 is not None and v <= q33: return "low"
        if q66 is not None and v <= q66: return "mid"
        if q90 is not None and v <= q90: return "high"
        return "very_high"
    return x.map(b)


def build_context_signature(df: pd.DataFrame, features: List[str]) -> pd.Series:
    parts = []
    preferred = []
    for fam, keys in FAMILY_KEYWORDS.items():
        match = [c for c in features if any(k in str(c).lower() for k in keys)]
        if match:
            preferred.append(match[0])
    preferred = list(dict.fromkeys(preferred))[:8]
    for c in preferred:
        parts.append(c + "=" + bucket_series(df[c]).astype(str))
    if not parts:
        return pd.Series(["generic_context"] * len(df), index=df.index)
    out = parts[0]
    for p in parts[1:]:
        out = out + "|" + p
    return out


def family_of_feature(c: str) -> str:
    cl = c.lower()
    for fam, keys in FAMILY_KEYWORDS.items():
        if any(k in cl for k in keys):
            return fam
    return "other"


def label_values(y: pd.Series) -> List[str]:
    vals = [str(v) for v in y.dropna().unique().tolist()]
    # Positive-ish labels first.
    order = ["UP", "DOWN", "CLEAN_LONG", "CLEAN_SHORT", "SPIKE", "BULL_TRAP", "BEAR_TRAP", "FLAT"]
    return sorted(vals, key=lambda v: (order.index(v) if v in order else 999, v))


def evaluate_rule(train: pd.DataFrame, test: pd.DataFrame, cond_col: str, cond_val: str, target: str, label: str, min_support: int, min_lift: float, max_gap: float) -> Dict[str, object]:
    base_train = (train[target].astype(str) == label).mean()
    base_test = (test[target].astype(str) == label).mean()
    tr = train[train[cond_col].astype(str) == cond_val]
    te = test[test[cond_col].astype(str) == cond_val]
    ntr, nte = len(tr), len(te)
    ptr = (tr[target].astype(str) == label).mean() if ntr else np.nan
    pte = (te[target].astype(str) == label).mean() if nte else np.nan
    lift_tr = ptr / max(base_train, 1e-9) if ntr else np.nan
    lift_te = pte / max(base_test, 1e-9) if nte else np.nan
    gap = abs(ptr - pte) if ntr and nte else np.nan
    accepted = bool(ntr >= min_support and nte >= max(10, min_support // 4) and lift_tr >= min_lift and lift_te >= 1.0 and gap <= max_gap)
    skepticism = "accepted" if accepted else "rejected"
    reasons = []
    if ntr < min_support: reasons.append("low_train_support")
    if nte < max(10, min_support // 4): reasons.append("low_test_support")
    if not np.isnan(lift_tr) and lift_tr < min_lift: reasons.append("weak_train_lift")
    if not np.isnan(lift_te) and lift_te < 1.0: reasons.append("no_oos_lift")
    if not np.isnan(gap) and gap > max_gap: reasons.append("unstable_train_test_gap")
    return {
        "target": target,
        "label": label,
        "condition": f"{cond_col} == {cond_val}",
        "condition_col": cond_col,
        "condition_value": cond_val,
        "train_support": ntr,
        "test_support": nte,
        "train_prob": float(ptr) if not np.isnan(ptr) else None,
        "test_prob": float(pte) if not np.isnan(pte) else None,
        "base_train_prob": float(base_train),
        "base_test_prob": float(base_test),
        "train_lift": float(lift_tr) if not np.isnan(lift_tr) else None,
        "test_lift": float(lift_te) if not np.isnan(lift_te) else None,
        "stability_gap": float(gap) if not np.isnan(gap) else None,
        "skepticism_status": skepticism,
        "rejection_reasons": ",".join(reasons),
    }


def make_rule_table(df: pd.DataFrame, targets: List[str], features: List[str], min_support: int, min_lift: float, max_gap: float) -> pd.DataFrame:
    work = df.copy()
    n = len(work)
    split = max(1, int(n * 0.70))
    train = work.iloc[:split].copy()
    test = work.iloc[split:].copy()
    cond_cols = []
    for c in features[:60]:
        bc = f"ctx__{c}"
        work[bc] = bucket_series(work[c]).astype(str)
        cond_cols.append(bc)
    # refresh train/test with bucket cols
    train = work.iloc[:split].copy(); test = work.iloc[split:].copy()

    # Add limited pair conditions across different families for human-like contexts.
    pair_cols = []
    for a, b in itertools.combinations(cond_cols[:18], 2):
        fa = family_of_feature(a.replace("ctx__", "")); fb = family_of_feature(b.replace("ctx__", ""))
        if fa == fb:
            continue
        pc = f"pair__{a.replace('ctx__','')}__AND__{b.replace('ctx__','')}"
        work[pc] = work[a].astype(str) + " & " + work[b].astype(str)
        pair_cols.append(pc)
        if len(pair_cols) >= 80:
            break
    train = work.iloc[:split].copy(); test = work.iloc[split:].copy()

    rows = []
    for target in targets:
        if target not in work.columns:
            continue
        for label in label_values(work[target]):
            for cc in cond_cols + pair_cols:
                vals = train[cc].value_counts().head(12).index.tolist()
                for v in vals:
                    rows.append(evaluate_rule(train, test, cc, str(v), target, label, min_support, min_lift, max_gap))
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    out["rank_score"] = out.apply(lambda r: (r.get("test_lift") or 0) * math.log1p(r.get("test_support") or 0) - 2.0 * (r.get("stability_gap") or 0), axis=1)
    out = out.sort_values(["skepticism_status", "rank_score"], ascending=[True, False]).reset_index(drop=True)
    return out


def build_case_memory(df: pd.DataFrame, targets: List[str], features: List[str], max_cases: int) -> pd.DataFrame:
    work = df.copy()
    work["cognitive_signature"] = build_context_signature(work, features)
    cols = []
    for c in ["time", "datetime", "broker_time", "utc_time"]:
        if c in work.columns:
            cols.append(c); break
    cols += ["cognitive_signature"] + targets
    for c in features[:25]:
        cols.append(c)
    cols = [c for c in dict.fromkeys(cols) if c in work.columns]
    sample = work[cols].tail(max_cases).copy()
    return sample


def write_jsonl(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build human-like cognitive astro memory with skeptical anti-overfit rule gates.")
    ap.add_argument("--dataset-csv", required=True)
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--targets", default="", help="Comma-separated labels. Default: all label_direction/clean/spike/trap columns.")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--min-support", type=int, default=80)
    ap.add_argument("--min-lift", type=float, default=1.10)
    ap.add_argument("--max-stability-gap", type=float, default=0.18)
    ap.add_argument("--max-cases", type=int, default=5000)
    args = ap.parse_args()

    common = Path(args.common_files)
    ds = Path(args.dataset_csv)
    if not ds.is_absolute():
        ds = common / ds
    df = read_csv_flexible(ds)
    if df.empty:
        raise SystemExit("Dataset is empty.")

    targets = [x.strip() for x in args.targets.split(",") if x.strip()] if args.targets.strip() else [
        c for c in df.columns if c.startswith("label_direction_") or c.startswith("label_clean_") or c.startswith("label_spike_") or c.startswith("label_bull_trap_") or c.startswith("label_bear_trap_")
    ]
    targets = [t for t in targets if t in df.columns]
    features = candidate_features(df, max_features=90)

    out_dir = Path(args.out_dir) if args.out_dir else common / "astro_ml" / "cognitive_memory" / args.asset / args.timeframe / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if not out_dir.is_absolute():
        out_dir = common / out_dir
    ensure_dir(out_dir)

    rules = make_rule_table(df, targets, features, args.min_support, args.min_lift, args.max_stability_gap)
    cases = build_case_memory(df, targets, features, args.max_cases)

    # High-level concept memory by feature family.
    concept_rows = []
    for fam in FAMILY_KEYWORDS.keys():
        fam_features = [f for f in features if family_of_feature(f) == fam]
        concept_rows.append({
            "asset": args.asset,
            "timeframe": args.timeframe,
            "family": fam,
            "feature_count": len(fam_features),
            "features": fam_features[:25],
            "created_utc": utc_now(),
            "interpretation_note": "candidate_context_family; trust only rules with skepticism_status=accepted and stable OOS lift",
        })

    rules_csv = out_dir / "skeptical_rules.csv"
    cases_csv = out_dir / "case_memory.csv"
    concepts_json = out_dir / "concept_memory.json"
    rules.to_csv(rules_csv, index=False, encoding="utf-8")
    cases.to_csv(cases_csv, index=False, encoding="utf-8")
    save_json(concepts_json, {"created_utc": utc_now(), "asset": args.asset, "timeframe": args.timeframe, "targets": targets, "features_used": features, "concept_families": concept_rows})
    write_jsonl(out_dir / "concept_memory.jsonl", concept_rows)

    accepted = rules[rules["skepticism_status"] == "accepted"].copy() if not rules.empty else pd.DataFrame()
    save_excel(out_dir / "cognitive_memory_report.xlsx", {
        "Summary": pd.DataFrame([{
            "asset": args.asset,
            "timeframe": args.timeframe,
            "dataset": str(ds),
            "rows": len(df),
            "targets": ",".join(targets),
            "features_considered": len(features),
            "rules_total": len(rules),
            "rules_accepted": len(accepted),
            "anti_overfit_contract": "rule accepted only with train support, OOS support, OOS lift, and bounded train/test gap",
        }]),
        "AcceptedRules": accepted.head(500),
        "AllRules": rules.head(5000),
        "CaseMemorySample": cases.head(1000),
        "ConceptFamilies": pd.DataFrame(concept_rows),
    })

    md = [f"# Cognitive Astro Memory - {args.asset} {args.timeframe}\n"]
    md.append("This report is deliberately skeptical. A pattern is not treated as learned knowledge unless it survives chronological holdout checks.\n")
    md.append(f"Dataset rows: `{len(df)}`  Targets: `{', '.join(targets)}`  Features considered: `{len(features)}`\n")
    md.append(f"Accepted skeptical rules: `{len(accepted)}` out of `{len(rules)}` candidate rules.\n")
    md.append("## Top accepted rules\n")
    if not accepted.empty:
        for _, r in accepted.head(25).iterrows():
            md.append(f"- `{r['target']}` -> `{r['label']}` when `{r['condition']}` | test_lift={r.get('test_lift'):.3f} support={int(r.get('test_support') or 0)} gap={r.get('stability_gap'):.3f}")
    else:
        md.append("No accepted rules yet. This is good if the data is too small; the system refused to hallucinate stable knowledge.")
    (out_dir / "COGNITIVE_MEMORY_REPORT.md").write_text("\n".join(md), encoding="utf-8")

    print(f"COGNITIVE_MEMORY_DIR={out_dir}")
    print(f"SKEPTICAL_RULES_CSV={rules_csv}")
    print(f"CASE_MEMORY_CSV={cases_csv}")
    print(f"COGNITIVE_MEMORY_REPORT={out_dir / 'COGNITIVE_MEMORY_REPORT.md'}")
    print(f"ACCEPTED_RULES={len(accepted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
