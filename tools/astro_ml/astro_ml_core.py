#!/usr/bin/env python3
"""
Decision Alpha Lab - EXP0016 Astro Meta Learner core utilities.

The module is intentionally dependency-light and deterministic. It turns a
mechanical astro feature store into a supervised research dataset, trains
walk-forward models, and persists a reusable knowledge/memory store.

Design goals:
- causal rows only: features at t, outcomes after t
- chronological evaluation only: no random split for market tests
- interpretable first: simple sklearn models, feature importances, rules
- reusable memory: every run writes model artifacts and learned lessons
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

try:
    import joblib
except Exception:  # pragma: no cover
    joblib = None

try:
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, classification_report, confusion_matrix, f1_score, log_loss
    from sklearn.model_selection import TimeSeriesSplit
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "scikit-learn is required for EXP0016. Install with: python -m pip install scikit-learn pandas numpy joblib openpyxl"
    ) from exc

EPS = 1e-12
DEFAULT_COMMON_FILES = Path(os.environ.get("APPDATA", r"C:\Users\ABN\AppData\Roaming")) / "MetaQuotes" / "Terminal" / "Common" / "Files"
DEFAULT_MEMORY_ROOT = DEFAULT_COMMON_FILES / "astro_ml" / "memory"
DEFAULT_REPORT_ROOT = DEFAULT_COMMON_FILES / "astro_ml" / "reports"

TIME_CANDIDATES = [
    "broker_time", "time", "datetime", "timestamp", "time_broker", "date", "utc_time", "open_time", "candle_time",
]
OPEN_CANDIDATES = ["open", "Open", "o", "bid_open", "ask_open"]
HIGH_CANDIDATES = ["high", "High", "h", "bid_high", "ask_high"]
LOW_CANDIDATES = ["low", "Low", "l", "bid_low", "ask_low"]
CLOSE_CANDIDATES = ["close", "Close", "c", "bid_close", "ask_close"]
VOLUME_CANDIDATES = ["tick_volume", "volume", "real_volume", "vol"]

NON_FEATURE_EXACT = {
    "time", "datetime", "timestamp", "date", "broker_time", "utc_time", "unix_utc", "jd_ut", "open_time", "candle_time",
    "open", "high", "low", "close", "Open", "High", "Low", "Close", "o", "h", "l", "c",
    "tick_volume", "volume", "real_volume", "spread", "source_file", "row_id",
}
NON_FEATURE_PREFIXES = (
    "future_", "label_", "target_", "outcome_", "mfe_", "mae_", "ret_", "clean_", "trap_", "spike_",
)

TEXT_META_COLUMNS = {
    "schema_version", "doctrine_id", "zodiac_mode", "body_universe", "orb_family", "feature_key", "summary",
    "astro_bias_text", "astro_path_text", "astro_signal_text", "natal_label", "natal_local_time", "natal_utc_time",
    "moon_phase_bucket", "moon_phase_half", "sect_name", "solar_quarter_name", "node_axis_sign", "nodal_state",
    "eclipse_state", "eclipse_family_phase", "mutual_reception_pairs", "house_system", "natal_house_system",
}

@dataclass
class OutcomeConfig:
    horizons: List[int] = field(default_factory=lambda: [30, 60, 120])
    direction_threshold_pct: float = 0.0010
    spike_threshold_pct: float = 0.0030
    trap_trigger_pct: float = 0.0015
    clean_min_mfe_pct: float = 0.0015
    clean_max_mae_pct: float = 0.0008
    price_entry: str = "close"

@dataclass
class FeatureConfig:
    max_categorical_uniques: int = 64
    keep_text_meta: bool = False
    drop_high_missing_pct: float = 0.97
    drop_constant: bool = True
    include_regex: Optional[str] = None
    exclude_regex: Optional[str] = None

@dataclass
class TrainConfig:
    model_type: str = "extra_trees"
    target: str = "label_direction_60"
    test_fraction: float = 0.25
    min_train_rows: int = 1000
    random_state: int = 42
    class_weight: str = "balanced"
    n_estimators: int = 500
    max_depth: Optional[int] = 8

@dataclass
class MemoryConfig:
    asset: str = "NAS100"
    timeframe: str = "M1"
    experiment_id: str = "EXP0016_ASTRO_META_LEARNER"
    memory_root: str = str(DEFAULT_MEMORY_ROOT)
    report_root: str = str(DEFAULT_REPORT_ROOT)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_run_id(parts: Sequence[str]) -> str:
    raw = "|".join(str(p) for p in parts) + "|" + utc_now_iso()
    return hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()[:12]


def ensure_dir(path: Path | str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_csv_flexible(path: Path | str, max_rows: Optional[int] = None) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    try:
        return pd.read_csv(path, encoding="utf-8-sig", nrows=max_rows, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="utf-8", nrows=max_rows, low_memory=False)


def find_col(columns: Sequence[str], candidates: Sequence[str], required: bool = True, role: str = "column") -> Optional[str]:
    lower_map = {str(c).lower(): c for c in columns}
    for c in candidates:
        if c in columns:
            return c
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    if required:
        raise ValueError(f"Could not find {role}. Tried: {candidates}. Available sample: {list(columns)[:30]}")
    return None


def normalize_time_column(df: pd.DataFrame, preferred: Optional[str] = None) -> Tuple[pd.DataFrame, str]:
    col = preferred if preferred else find_col(df.columns, TIME_CANDIDATES, required=True, role="time column")
    out = df.copy()
    out[col] = pd.to_datetime(out[col], errors="coerce")
    out = out.dropna(subset=[col]).sort_values(col).reset_index(drop=True)
    return out, col


def normalize_price_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    cols = df.columns
    mapping = {
        "open": find_col(cols, OPEN_CANDIDATES, required=False, role="open"),
        "high": find_col(cols, HIGH_CANDIDATES, required=False, role="high"),
        "low": find_col(cols, LOW_CANDIDATES, required=False, role="low"),
        "close": find_col(cols, CLOSE_CANDIDATES, required=False, role="close"),
        "volume": find_col(cols, VOLUME_CANDIDATES, required=False, role="volume"),
    }
    if mapping["close"] is None:
        raise ValueError("No close column found. Provide a price CSV with open/high/low/close or add close to the astro CSV.")
    out = df.copy()
    # If high/low/open missing, fall back to close; enough for direction labels, not enough for path labels.
    for k in ["open", "high", "low"]:
        if mapping[k] is None:
            out[f"__{k}"] = out[mapping["close"]]
            mapping[k] = f"__{k}"
    for k in ["open", "high", "low", "close"]:
        out[mapping[k]] = pd.to_numeric(out[mapping[k]], errors="coerce")
    return out, mapping


def merge_astro_price(
    astro_df: pd.DataFrame,
    price_df: Optional[pd.DataFrame],
    astro_time_col: str,
    price_time_col: Optional[str] = None,
    tolerance: str = "30s",
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    if price_df is None:
        price_ready, price_cols = normalize_price_columns(astro_df)
        return price_ready, price_cols

    price_ready, pt = normalize_time_column(price_df, price_time_col)
    price_ready, price_cols = normalize_price_columns(price_ready)

    price_keep = [pt, price_cols["open"], price_cols["high"], price_cols["low"], price_cols["close"]]
    if price_cols.get("volume") is not None:
        price_keep.append(price_cols["volume"])
    price_keep = list(dict.fromkeys(price_keep))
    p = price_ready[price_keep].copy()

    rename = {pt: astro_time_col}
    for role, col in price_cols.items():
        if col is None:
            continue
        rename[col] = role if role != "volume" else "tick_volume"
    p = p.rename(columns=rename)
    a = astro_df.copy().sort_values(astro_time_col)
    p = p.sort_values(astro_time_col)

    merged = pd.merge_asof(
        a,
        p,
        on=astro_time_col,
        direction="nearest",
        tolerance=pd.Timedelta(tolerance),
    )
    missing = merged["close"].isna().mean()
    if missing > 0.01:
        raise ValueError(f"Price merge missing ratio too high: {missing:.2%}. Check time zones / tolerance.")
    merged = merged.dropna(subset=["close"]).reset_index(drop=True)
    return merged, {"open": "open", "high": "high", "low": "low", "close": "close", "volume": "tick_volume" if "tick_volume" in merged.columns else None}


def add_future_outcomes(df: pd.DataFrame, price_cols: Dict[str, str], cfg: OutcomeConfig) -> pd.DataFrame:
    out = df.copy()
    close = pd.to_numeric(out[price_cols["close"]], errors="coerce")
    high = pd.to_numeric(out[price_cols["high"]], errors="coerce")
    low = pd.to_numeric(out[price_cols["low"]], errors="coerce")
    for h in cfg.horizons:
        future_close = close.shift(-h)
        ret = (future_close - close) / close.replace(0, np.nan)
        out[f"ret_{h}"] = ret
        out[f"label_direction_{h}"] = np.where(ret > cfg.direction_threshold_pct, "UP", np.where(ret < -cfg.direction_threshold_pct, "DOWN", "FLAT"))

        # Forward max/min over the next h bars excluding current bar.
        f_high = pd.concat([high.shift(-i) for i in range(1, h + 1)], axis=1).max(axis=1)
        f_low = pd.concat([low.shift(-i) for i in range(1, h + 1)], axis=1).min(axis=1)
        mfe_long = (f_high - close) / close.replace(0, np.nan)
        mae_long = (close - f_low) / close.replace(0, np.nan)
        mfe_short = (close - f_low) / close.replace(0, np.nan)
        mae_short = (f_high - close) / close.replace(0, np.nan)
        out[f"mfe_long_{h}"] = mfe_long
        out[f"mae_long_{h}"] = mae_long
        out[f"mfe_short_{h}"] = mfe_short
        out[f"mae_short_{h}"] = mae_short
        out[f"clean_long_score_{h}"] = mfe_long / (mae_long + EPS)
        out[f"clean_short_score_{h}"] = mfe_short / (mae_short + EPS)
        out[f"label_clean_long_{h}"] = np.where((mfe_long >= cfg.clean_min_mfe_pct) & (mae_long <= cfg.clean_max_mae_pct), "CLEAN_LONG", "NOT_CLEAN_LONG")
        out[f"label_clean_short_{h}"] = np.where((mfe_short >= cfg.clean_min_mfe_pct) & (mae_short <= cfg.clean_max_mae_pct), "CLEAN_SHORT", "NOT_CLEAN_SHORT")

        range_pct = (f_high - f_low) / close.replace(0, np.nan)
        out[f"future_range_pct_{h}"] = range_pct
        out[f"label_spike_{h}"] = np.where(range_pct >= cfg.spike_threshold_pct, "SPIKE", "NO_SPIKE")

        # Trap labels are intentionally mechanical. Bull trap: enough upward excursion but bad close / deep adverse finish.
        out[f"label_bull_trap_{h}"] = np.where((mfe_long >= cfg.trap_trigger_pct) & (ret < -cfg.direction_threshold_pct), "BULL_TRAP", "NO_BULL_TRAP")
        out[f"label_bear_trap_{h}"] = np.where((mfe_short >= cfg.trap_trigger_pct) & (ret > cfg.direction_threshold_pct), "BEAR_TRAP", "NO_BEAR_TRAP")

    max_h = max(cfg.horizons) if cfg.horizons else 0
    if max_h > 0:
        out = out.iloc[:-max_h].reset_index(drop=True)
    return out


def infer_feature_columns(df: pd.DataFrame, cfg: FeatureConfig, target: Optional[str] = None) -> Tuple[List[str], List[str], List[str]]:
    include_re = re.compile(cfg.include_regex) if cfg.include_regex else None
    exclude_re = re.compile(cfg.exclude_regex) if cfg.exclude_regex else None
    numeric_features: List[str] = []
    categorical_features: List[str] = []
    dropped: List[str] = []

    for col in df.columns:
        if target and col == target:
            dropped.append(col); continue
        if col in NON_FEATURE_EXACT or col.lower() in {c.lower() for c in NON_FEATURE_EXACT}:
            dropped.append(col); continue
        if any(col.startswith(p) for p in NON_FEATURE_PREFIXES):
            dropped.append(col); continue
        if include_re and not include_re.search(col):
            dropped.append(col); continue
        if exclude_re and exclude_re.search(col):
            dropped.append(col); continue
        missing_pct = df[col].isna().mean()
        if missing_pct >= cfg.drop_high_missing_pct:
            dropped.append(col); continue
        nunique = df[col].nunique(dropna=True)
        if cfg.drop_constant and nunique <= 1:
            dropped.append(col); continue
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_features.append(col)
        else:
            if (col in TEXT_META_COLUMNS) and not cfg.keep_text_meta:
                dropped.append(col); continue
            if nunique <= cfg.max_categorical_uniques:
                categorical_features.append(col)
            else:
                dropped.append(col)
    return numeric_features, categorical_features, dropped


def make_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    num_pipe = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    cat_pipe = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    transformers = []
    if numeric_features:
        transformers.append(("num", num_pipe, numeric_features))
    if categorical_features:
        transformers.append(("cat", cat_pipe, categorical_features))
    if not transformers:
        raise ValueError("No usable features found.")
    return ColumnTransformer(transformers=transformers, remainder="drop", verbose_feature_names_out=True)


def make_model(cfg: TrainConfig):
    mt = cfg.model_type.lower()
    if mt in {"extra_trees", "et"}:
        return ExtraTreesClassifier(
            n_estimators=cfg.n_estimators,
            random_state=cfg.random_state,
            class_weight=cfg.class_weight,
            max_depth=cfg.max_depth,
            min_samples_leaf=25,
            n_jobs=-1,
        )
    if mt in {"random_forest", "rf"}:
        return RandomForestClassifier(
            n_estimators=cfg.n_estimators,
            random_state=cfg.random_state,
            class_weight=cfg.class_weight,
            max_depth=cfg.max_depth,
            min_samples_leaf=25,
            n_jobs=-1,
        )
    if mt in {"gradient_boosting", "gb"}:
        return GradientBoostingClassifier(random_state=cfg.random_state, max_depth=3)
    if mt in {"logit", "logistic", "logistic_regression"}:
        return LogisticRegression(max_iter=2000, class_weight=cfg.class_weight, n_jobs=-1, multi_class="auto")
    raise ValueError(f"Unknown model_type={cfg.model_type}")


def build_pipeline(numeric_features: List[str], categorical_features: List[str], cfg: TrainConfig) -> Pipeline:
    return Pipeline(steps=[("pre", make_preprocessor(numeric_features, categorical_features)), ("model", make_model(cfg))])


def chronological_train_test_split(df: pd.DataFrame, target: str, test_fraction: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    clean = df.dropna(subset=[target]).reset_index(drop=True)
    if len(clean) < 10:
        raise ValueError(f"Too few rows after target cleanup: {len(clean)}")
    split = int(len(clean) * (1.0 - test_fraction))
    split = max(1, min(split, len(clean) - 1))
    return clean.iloc[:split].copy(), clean.iloc[split:].copy()


def evaluate_predictions(y_true: Sequence[Any], y_pred: Sequence[Any], labels: Optional[List[str]] = None) -> Dict[str, Any]:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if labels is None:
        labels = sorted(list(set(y_true) | set(y_pred)))
    metrics: Dict[str, Any] = {
        "n": len(y_true),
        "labels": labels,
        "accuracy": float(accuracy_score(y_true, y_pred)) if y_true else None,
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)) if len(set(y_true)) > 1 else None,
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)) if y_true else None,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist() if y_true else [],
        "classification_report": classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0) if y_true else {},
    }
    return metrics


def evaluate_probability_quality(y_true: Sequence[Any], proba: pd.DataFrame, prefix: str = "proba") -> Dict[str, Any]:
    y_true = [str(x) for x in y_true]
    if not y_true or proba.empty:
        return {"probability_rows": 0}

    classes: List[str] = []
    arrays: List[np.ndarray] = []
    for c in proba.columns:
        if not str(c).startswith(prefix + "_"):
            continue
        cls = str(c).replace(prefix + "_", "", 1)
        classes.append(cls)
        arrays.append(pd.to_numeric(proba[c], errors="coerce").fillna(0.0).to_numpy(dtype=float))
    if not classes or not arrays:
        return {"probability_rows": 0}

    p = np.vstack(arrays).T
    row_sum = p.sum(axis=1)
    row_sum[row_sum <= 0.0] = 1.0
    p = p / row_sum.reshape(-1, 1)

    out: Dict[str, Any] = {
        "probability_rows": int(len(y_true)),
        "probability_classes": classes,
        "mean_max_probability": float(np.max(p, axis=1).mean()),
    }
    try:
        out["log_loss"] = float(log_loss(y_true, p, labels=classes))
    except Exception:
        out["log_loss"] = None

    brier_parts = []
    for i, cls in enumerate(classes):
        actual = np.asarray([1 if y == cls else 0 for y in y_true], dtype=float)
        try:
            brier_parts.append(float(brier_score_loss(actual, p[:, i])))
        except Exception:
            pass
    out["brier_macro"] = float(np.mean(brier_parts)) if brier_parts else None
    return out


def get_transformed_feature_names(pipe: Pipeline, numeric_features: List[str], categorical_features: List[str]) -> List[str]:
    pre = pipe.named_steps["pre"]
    try:
        names = pre.get_feature_names_out().tolist()
    except Exception:
        names = [f"num__{x}" for x in numeric_features]
        if categorical_features:
            names += [f"cat__{x}" for x in categorical_features]
    return names


def aggregate_feature_importance(pipe: Pipeline, numeric_features: List[str], categorical_features: List[str]) -> pd.DataFrame:
    model = pipe.named_steps["model"]
    names = get_transformed_feature_names(pipe, numeric_features, categorical_features)
    if hasattr(model, "feature_importances_"):
        imp = np.asarray(model.feature_importances_, dtype=float)
    elif hasattr(model, "coef_"):
        coef = np.asarray(model.coef_, dtype=float)
        imp = np.mean(np.abs(coef), axis=0) if coef.ndim > 1 else np.abs(coef)
    else:
        return pd.DataFrame(columns=["raw_feature", "transformed_feature", "importance"])
    n = min(len(names), len(imp))
    rows = []
    for name, val in zip(names[:n], imp[:n]):
        raw = name
        if name.startswith("num__"):
            raw = name.replace("num__", "", 1)
        elif name.startswith("cat__"):
            raw = name.replace("cat__", "", 1).split("_")[0]
        rows.append({"raw_feature": raw, "transformed_feature": name, "importance": float(val)})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    agg = df.groupby("raw_feature", as_index=False)["importance"].sum().sort_values("importance", ascending=False)
    return agg


def save_json(path: Path | str, data: Any) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def load_json(path: Path | str) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def save_excel(path: Path | str, sheets: Dict[str, pd.DataFrame]) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    try:
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            for name, df in sheets.items():
                safe_name = name[:31]
                df.to_excel(writer, sheet_name=safe_name, index=False)
    except Exception:
        # Always emit CSV mirrors if Excel dependency fails.
        stem = path.with_suffix("")
        for name, df in sheets.items():
            df.to_csv(stem.parent / f"{stem.name}_{name}.csv", index=False, encoding="utf-8")
        raise


def memory_paths(cfg: MemoryConfig, run_id: str) -> Dict[str, Path]:
    root = Path(cfg.memory_root) / cfg.asset / cfg.timeframe
    run = root / "runs" / run_id
    return {
        "root": root,
        "run": run,
        "index": root / "memory_index.csv",
        "knowledge_jsonl": root / "knowledge_memory.jsonl",
        "latest_pointer": root / "latest_run.txt",
    }


def append_memory_index(cfg: MemoryConfig, run_id: str, row: Dict[str, Any]) -> None:
    paths = memory_paths(cfg, run_id)
    ensure_dir(paths["root"])
    index = paths["index"]
    row = {"run_id": run_id, "created_utc": utc_now_iso(), **row}
    exists = index.exists()
    with index.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)
    paths["latest_pointer"].write_text(run_id, encoding="utf-8")


def append_knowledge(cfg: MemoryConfig, run_id: str, lessons: List[Dict[str, Any]]) -> None:
    paths = memory_paths(cfg, run_id)
    ensure_dir(paths["root"])
    with paths["knowledge_jsonl"].open("a", encoding="utf-8") as f:
        for lesson in lessons:
            f.write(json.dumps({"run_id": run_id, "created_utc": utc_now_iso(), **lesson}, ensure_ascii=False, default=str) + "\n")


def generate_simple_lessons(importance: pd.DataFrame, metrics: Dict[str, Any], target: str, top_n: int = 25) -> List[Dict[str, Any]]:
    lessons: List[Dict[str, Any]] = []
    if not importance.empty:
        for i, row in importance.head(top_n).iterrows():
            lessons.append({
                "lesson_type": "feature_importance",
                "target": target,
                "rank": int(len(lessons) + 1),
                "feature": row["raw_feature"],
                "importance": float(row["importance"]),
                "interpretation": f"Feature {row['raw_feature']} was among the strongest learned mechanical astro drivers for {target} in this run.",
            })
    lessons.append({
        "lesson_type": "model_performance",
        "target": target,
        "accuracy": metrics.get("accuracy"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "f1_macro": metrics.get("f1_macro"),
        "interpretation": "Use this run only if out-of-sample metrics beat naive baselines and remain stable across walk-forward folds.",
    })
    return lessons


def class_probability_frame(pipe: Pipeline, X: pd.DataFrame, prefix: str = "proba") -> pd.DataFrame:
    model = pipe.named_steps["model"]
    if not hasattr(model, "predict_proba"):
        return pd.DataFrame(index=X.index)
    proba = pipe.predict_proba(X)
    classes = list(model.classes_)
    return pd.DataFrame({f"{prefix}_{str(c)}": proba[:, i] for i, c in enumerate(classes)}, index=X.index)
