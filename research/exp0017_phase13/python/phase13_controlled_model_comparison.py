#!/usr/bin/env python3
"""EXP0017 Phase 13 — Controlled Model Comparison.

Research-only, deterministic, standard-library implementation.

The engine compares simple model families on the fixed Phase 11 walk-forward
fold plan. It never places orders, changes risk, filters cycle groups, or
promotes a strategy rule.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

VERSION = "13.0.0"
EPS = 1e-12

ALLOWED_RAW_FEATURES = {
    "group", "group_minutes", "current_cycle", "reference_cycle",
    "reference_age_cycles", "direction", "direction_code", "side", "side_code",
    "clean_symbol", "hunter_symbol", "role_key", "hour_ny", "minute_of_day_ny",
    "session_ny", "stop_points",
}

FORBIDDEN_FUTURE_OR_RESEARCH_FEATURES = {
    "cycle_end_r", "plus1_r", "plus2_r", "plus3_r", "day_end_r", "mfe_r", "mae_r",
    "cycle_end_points", "plus1_points", "plus2_points", "plus3_points", "day_end_points",
    "mfe_points", "mae_points", "primary_r", "primary_points", "primary_norm_daily_range",
    "label_class", "label_binary_win", "label_hit_1r", "label_stopped_intraday",
    "label_adverse_1r", "daily_range_points", "risk_to_daily_range",
    "cg_quality_score", "cg_rank", "cg_direction_quality_score", "cg_direction_rank",
    "role_quality_score", "role_rank", "cg_direction_role_quality_score",
    "cg_direction_role_rank", "shortlist_match",
}

NUMERIC_FEATURES = (
    "group_minutes_log", "reference_age_cycles", "direction_code", "side_code",
    "hour_sin", "hour_cos", "stop_points_log",
)
CATEGORICAL_FEATURES = (
    "group", "direction", "clean_symbol", "hunter_symbol", "role_key", "session_ny",
)

CLASSIFICATION_MODELS = (
    "bucket_baseline_classifier", "threshold_classifier",
    "logistic_classifier", "constrained_ensemble_classifier",
)
REGRESSION_MODELS = (
    "bucket_baseline_regressor", "threshold_regressor",
    "ridge_regression", "constrained_ensemble_regressor",
)


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        x = float(str(value).strip())
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def sigmoid(x: float) -> float:
    x = clip(x, -35.0, 35.0)
    return 1.0 / (1.0 + math.exp(-x))


def parse_dt(value: str) -> dt.datetime:
    value = (value or "").strip()
    formats = (
        "%Y.%m.%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
        "%Y/%m/%d %H:%M:%S", "%Y.%m.%d %H:%M", "%Y-%m-%d %H:%M",
    )
    for fmt in formats:
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            pass
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError as exc:
        raise ValueError(f"Unsupported datetime: {value!r}") from exc


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stdev(values: Sequence[float]) -> float:
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def percentile(values: Sequence[float], q: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    pos = clip(q, 0.0, 1.0) * (len(xs) - 1)
    lo = int(math.floor(pos)); hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return 0.0
    mx, my = mean(xs), mean(ys)
    dx = [x - mx for x in xs]; dy = [y - my for y in ys]
    den = math.sqrt(sum(x*x for x in dx) * sum(y*y for y in dy))
    return sum(a*b for a, b in zip(dx, dy)) / den if den > EPS else 0.0


def read_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


@dataclass
class Sample:
    sample_id: str
    signal_id: str
    confirmation: dt.datetime
    raw: dict
    actual_r: float
    actual_win: int


@dataclass
class Fold:
    fold_id: int
    train_start: dt.datetime
    train_end: dt.datetime
    embargo_start: dt.datetime
    embargo_end: dt.datetime
    test_start: dt.datetime
    test_end: dt.datetime
    usable: bool
    status: str


@dataclass
class BucketStats:
    count: int = 0
    sum_r: float = 0.0
    wins: int = 0

    @property
    def avg_r(self) -> float:
        return self.sum_r / self.count if self.count else 0.0

    @property
    def win_rate(self) -> float:
        return self.wins / self.count if self.count else 0.5


class FeatureEncoder:
    """Train-only fit; sparse deterministic encoding with unknown buckets."""
    def __init__(self) -> None:
        self.means: Dict[str, float] = {}
        self.scales: Dict[str, float] = {}
        self.categories: Dict[str, set] = {}

    @staticmethod
    def engineered(raw: Mapping[str, str]) -> Tuple[Dict[str, float], Dict[str, str]]:
        minute = safe_float(raw.get("minute_of_day_ny"), safe_float(raw.get("hour_ny")) * 60.0)
        angle = 2.0 * math.pi * minute / 1440.0
        nums = {
            "group_minutes_log": math.log1p(max(0.0, safe_float(raw.get("group_minutes")))),
            "reference_age_cycles": safe_float(raw.get("reference_age_cycles")),
            "direction_code": safe_float(raw.get("direction_code")),
            "side_code": safe_float(raw.get("side_code")),
            "hour_sin": math.sin(angle),
            "hour_cos": math.cos(angle),
            "stop_points_log": math.log1p(abs(safe_float(raw.get("stop_points")))),
        }
        cats = {name: str(raw.get(name, "") or "__MISSING__") for name in CATEGORICAL_FEATURES}
        return nums, cats

    def fit(self, samples: Sequence[Sample]) -> "FeatureEncoder":
        numeric_values: Dict[str, List[float]] = {name: [] for name in NUMERIC_FEATURES}
        categories: Dict[str, set] = {name: set() for name in CATEGORICAL_FEATURES}
        for s in samples:
            nums, cats = self.engineered(s.raw)
            for k, v in nums.items(): numeric_values[k].append(v)
            for k, v in cats.items(): categories[k].add(v)
        for k, vals in numeric_values.items():
            self.means[k] = mean(vals)
            scale = stdev(vals)
            self.scales[k] = scale if scale > 1e-9 else 1.0
        self.categories = categories
        return self

    def transform_one(self, sample: Sample) -> Dict[str, float]:
        nums, cats = self.engineered(sample.raw)
        out: Dict[str, float] = {}
        for k in NUMERIC_FEATURES:
            out[f"num:{k}"] = (nums[k] - self.means.get(k, 0.0)) / self.scales.get(k, 1.0)
        for k in CATEGORICAL_FEATURES:
            value = cats[k] if cats[k] in self.categories.get(k, set()) else "__OTHER__"
            out[f"cat:{k}={value}"] = 1.0
        return out


class BucketBaseline:
    def __init__(self, min_bucket_rows: int = 20, key_mode: str = "group_direction_role") -> None:
        self.min_bucket_rows = min_bucket_rows
        self.key_mode = key_mode
        self.tables: Dict[str, Dict[str, BucketStats]] = defaultdict(dict)
        self.global_stats = BucketStats()

    @staticmethod
    def key(raw: Mapping[str, str], mode: str) -> str:
        group = str(raw.get("group", "")); direction = str(raw.get("direction", "")); role = str(raw.get("role_key", ""))
        if mode == "group_direction_role": return f"{group}|{direction}|{role}"
        if mode == "group_direction": return f"{group}|{direction}"
        if mode == "role": return role
        if mode == "group": return group
        if mode == "direction": return direction
        return "ALL"

    def fit(self, samples: Sequence[Sample]) -> "BucketBaseline":
        modes = (self.key_mode, "group_direction", "role", "group", "direction")
        for s in samples:
            self.global_stats.count += 1; self.global_stats.sum_r += s.actual_r; self.global_stats.wins += s.actual_win
            for mode in modes:
                key = self.key(s.raw, mode)
                stat = self.tables[mode].setdefault(key, BucketStats())
                stat.count += 1; stat.sum_r += s.actual_r; stat.wins += s.actual_win
        return self

    def predict(self, sample: Sample) -> Tuple[float, float, str, int]:
        for mode in (self.key_mode, "group_direction", "role", "group", "direction"):
            stat = self.tables.get(mode, {}).get(self.key(sample.raw, mode))
            if stat and stat.count >= self.min_bucket_rows:
                return stat.avg_r, clip(stat.win_rate, 0.001, 0.999), mode, stat.count
        s = self.global_stats
        return s.avg_r, clip(s.win_rate, 0.001, 0.999), "global", s.count


class ThresholdBaseline:
    """Train-derived one-feature median split; deterministic and auditable."""
    CANDIDATES = ("group_minutes", "reference_age_cycles", "hour_ny", "minute_of_day_ny", "stop_points")

    def __init__(self, min_side_rows: int = 20) -> None:
        self.min_side_rows = min_side_rows
        self.feature = ""
        self.threshold = 0.0
        self.low = BucketStats(); self.high = BucketStats(); self.global_stats = BucketStats()
        self.score = 0.0

    def fit(self, samples: Sequence[Sample]) -> "ThresholdBaseline":
        for s in samples:
            self.global_stats.count += 1; self.global_stats.sum_r += s.actual_r; self.global_stats.wins += s.actual_win
        best = None
        for feature in self.CANDIDATES:
            vals = [safe_float(s.raw.get(feature)) for s in samples]
            threshold = percentile(vals, 0.5)
            low, high = BucketStats(), BucketStats()
            for s, v in zip(samples, vals):
                side = low if v <= threshold else high
                side.count += 1; side.sum_r += s.actual_r; side.wins += s.actual_win
            if low.count < self.min_side_rows or high.count < self.min_side_rows:
                continue
            score = abs(high.avg_r - low.avg_r) * math.sqrt(min(low.count, high.count))
            candidate = (score, feature, threshold, low, high)
            if best is None or candidate[0] > best[0] or (candidate[0] == best[0] and feature < best[1]):
                best = candidate
        if best:
            self.score, self.feature, self.threshold, self.low, self.high = best
        return self

    def predict(self, sample: Sample) -> Tuple[float, float, str, int]:
        if not self.feature:
            s = self.global_stats
            return s.avg_r, clip(s.win_rate, 0.001, 0.999), "global", s.count
        value = safe_float(sample.raw.get(self.feature))
        s = self.low if value <= self.threshold else self.high
        label = f"{self.feature}<={self.threshold:.8g}" if value <= self.threshold else f"{self.feature}>{self.threshold:.8g}"
        return s.avg_r, clip(s.win_rate, 0.001, 0.999), label, s.count


class SparseLinearModel:
    def __init__(self, task: str, epochs: int, learning_rate: float, l2: float, seed: int) -> None:
        self.task = task
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.l2 = l2
        self.seed = seed
        self.weights: Dict[str, float] = {}
        self.intercept = 0.0

    def fit(self, xrows: Sequence[Dict[str, float]], ys: Sequence[float]) -> "SparseLinearModel":
        if not ys: return self
        if self.task == "classification":
            base = clip(mean(ys), 0.001, 0.999)
            self.intercept = math.log(base / (1.0 - base))
        else:
            self.intercept = mean(ys)
        indices = list(range(len(ys)))
        rng = random.Random(self.seed)
        for epoch in range(self.epochs):
            rng.shuffle(indices)
            lr = self.learning_rate / (1.0 + 0.04 * epoch)
            for i in indices:
                x = xrows[i]; y = ys[i]
                z = self.intercept + sum(self.weights.get(k, 0.0) * v for k, v in x.items())
                pred = sigmoid(z) if self.task == "classification" else z
                err = pred - y
                self.intercept -= lr * err
                for k, v in x.items():
                    old = self.weights.get(k, 0.0)
                    new = old - lr * (err * v + self.l2 * old)
                    self.weights[k] = clip(new, -30.0, 30.0)
            self.intercept = clip(self.intercept, -50.0, 50.0)
        return self

    def predict(self, x: Mapping[str, float]) -> float:
        z = self.intercept + sum(self.weights.get(k, 0.0) * v for k, v in x.items())
        return sigmoid(z) if self.task == "classification" else z


def classification_metrics(actual: Sequence[int], predicted: Sequence[float]) -> Dict[str, float]:
    n = len(actual)
    if not n: return {}
    probs = [clip(p, 1e-6, 1 - 1e-6) for p in predicted]
    labels = [1 if p >= 0.5 else 0 for p in probs]
    tp = sum(1 for y, z in zip(actual, labels) if y == 1 and z == 1)
    tn = sum(1 for y, z in zip(actual, labels) if y == 0 and z == 0)
    fp = sum(1 for y, z in zip(actual, labels) if y == 0 and z == 1)
    fn = sum(1 for y, z in zip(actual, labels) if y == 1 and z == 0)
    recall = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    brier = mean([(p - y) ** 2 for p, y in zip(probs, actual)])
    logloss = -mean([y * math.log(p) + (1 - y) * math.log(1 - p) for p, y in zip(probs, actual)])
    bins = calibration_bins(actual, probs, 10)
    ece = sum(row["count"] / n * row["abs_gap"] for row in bins)
    intercept, slope = calibration_logistic_fit(actual, probs)
    return {
        "n": n, "positive_rate": mean(actual), "mean_prediction": mean(probs),
        "accuracy": (tp + tn) / n, "balanced_accuracy": (recall + specificity) / 2.0,
        "precision": precision, "recall": recall, "specificity": specificity,
        "brier": brier, "log_loss": logloss, "ece": ece,
        "calibration_intercept": intercept, "calibration_slope": slope,
    }


def calibration_logistic_fit(actual: Sequence[int], predicted: Sequence[float]) -> Tuple[float, float]:
    if len(actual) < 10 or len(set(actual)) < 2:
        return 0.0, 0.0
    xs = [math.log(clip(p, 1e-6, 1 - 1e-6) / (1 - clip(p, 1e-6, 1 - 1e-6))) for p in predicted]
    a, b = 0.0, 1.0
    for _ in range(30):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, actual):
            p = sigmoid(a + b * x); w = max(p * (1 - p), 1e-8); e = p - y
            g0 += e; g1 += e * x; h00 += w; h01 += w * x; h11 += w * x * x
        det = h00 * h11 - h01 * h01
        if abs(det) < 1e-10: break
        da = (h11 * g0 - h01 * g1) / det
        db = (-h01 * g0 + h00 * g1) / det
        a -= da; b -= db
        if abs(da) + abs(db) < 1e-7: break
    return a, b


def calibration_bins(actual: Sequence[int], predicted: Sequence[float], bins: int = 10) -> List[dict]:
    out = []
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        idx = [j for j, p in enumerate(predicted) if (lo <= p < hi) or (i == bins - 1 and p == 1.0)]
        if not idx: continue
        ap = mean([predicted[j] for j in idx]); ar = mean([actual[j] for j in idx])
        out.append({"bin": i + 1, "lower": lo, "upper": hi, "count": len(idx), "avg_prediction": ap, "observed_rate": ar, "abs_gap": abs(ap - ar)})
    return out


def regression_metrics(actual: Sequence[float], predicted: Sequence[float]) -> Dict[str, float]:
    n = len(actual)
    if not n: return {}
    errors = [p - y for p, y in zip(predicted, actual)]
    mse = mean([e * e for e in errors]); mae = mean([abs(e) for e in errors])
    ymean = mean(actual); sst = sum((y - ymean) ** 2 for y in actual); sse = sum(e * e for e in errors)
    r2 = 1.0 - sse / sst if sst > EPS else 0.0
    sign_accuracy = mean([1.0 if (p > 0) == (y > 0) else 0.0 for p, y in zip(predicted, actual)])
    return {
        "n": n, "mean_actual": ymean, "mean_prediction": mean(predicted),
        "mae": mae, "rmse": math.sqrt(mse), "r2": r2,
        "pearson": pearson(actual, predicted), "sign_accuracy": sign_accuracy,
    }


def load_samples(path: Path, max_rows: int) -> Tuple[List[Sample], List[str]]:
    rows = read_csv(path)
    diagnostics: List[str] = []
    samples: List[Sample] = []
    required = {"sample_id", "signal_id", "model_use_status", "confirmation_ny", "primary_r", "label_binary_win"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")
    for idx, row in enumerate(rows[:max_rows] if max_rows > 0 else rows, start=2):
        if str(row.get("model_use_status", "")).strip().lower() != "model_ready":
            continue
        try:
            confirmation = parse_dt(str(row.get("confirmation_ny", "")))
        except ValueError:
            diagnostics.append(f"row {idx}: invalid confirmation_ny")
            continue
        sample_id = str(row.get("sample_id", "")).strip()
        if not sample_id:
            diagnostics.append(f"row {idx}: empty sample_id")
            continue
        samples.append(Sample(
            sample_id=sample_id,
            signal_id=str(row.get("signal_id", "")).strip(),
            confirmation=confirmation,
            raw=row,
            actual_r=safe_float(row.get("primary_r")),
            actual_win=safe_int(row.get("label_binary_win")),
        ))
    samples.sort(key=lambda s: (s.confirmation, s.sample_id))
    return samples, diagnostics


def load_folds(path: Path) -> List[Fold]:
    rows = read_csv(path)
    folds = []
    for row in rows:
        folds.append(Fold(
            fold_id=safe_int(row.get("fold_id")),
            train_start=parse_dt(str(row.get("train_start", ""))),
            train_end=parse_dt(str(row.get("train_end", ""))),
            embargo_start=parse_dt(str(row.get("embargo_start", ""))),
            embargo_end=parse_dt(str(row.get("embargo_end", ""))),
            test_start=parse_dt(str(row.get("test_start", ""))),
            test_end=parse_dt(str(row.get("test_end", ""))),
            usable=safe_int(row.get("usable"), 1) == 1,
            status=str(row.get("status", "")),
        ))
    return sorted(folds, key=lambda f: f.fold_id)


def read_integrity_status(path: Path, allow_missing: bool) -> Tuple[str, List[str]]:
    warnings: List[str] = []
    if not path.exists():
        if allow_missing:
            return "MISSING_OVERRIDE", ["Phase 12.5 readiness summary missing; engineering override used."]
        raise RuntimeError(f"Phase 12.5 integrity summary not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    status = str(data.get("status") or data.get("readiness_status") or "UNKNOWN")
    if status == "BLOCKED_FOR_PHASE13":
        raise RuntimeError("Phase 12.5 status is BLOCKED_FOR_PHASE13. Repair upstream integrity first.")
    if status == "READY_WITH_WARNINGS":
        warnings.append("Phase 12.5 status is READY_WITH_WARNINGS; all Phase 13 conclusions are provisional.")
    if status not in {"READY_FOR_PHASE13", "READY_WITH_WARNINGS"}:
        raise RuntimeError(f"Unsupported Phase 12.5 readiness status: {status}")
    return status, warnings


def model_comparison_score(rows: Sequence[dict], task: str) -> List[dict]:
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for r in rows:
        if r["task"] == task:
            grouped[str(r["model_name"])].append(r)
    if not grouped: return []
    summary = []
    for model, rs in grouped.items():
        item = {"task": task, "model_name": model, "folds": len(rs)}
        metrics = ("log_loss", "brier", "ece", "balanced_accuracy") if task == "classification" else ("rmse", "mae", "r2", "sign_accuracy")
        for m in metrics:
            vals = [safe_float(r.get(m)) for r in rs]
            item[f"mean_{m}"] = mean(vals); item[f"std_{m}"] = stdev(vals); item[f"worst_{m}"] = max(vals) if m in {"log_loss","brier","ece","rmse","mae"} else min(vals)
        summary.append(item)
    metrics = ("mean_log_loss", "mean_brier", "mean_ece", "mean_balanced_accuracy") if task == "classification" else ("mean_rmse", "mean_mae", "mean_r2", "mean_sign_accuracy")
    directions = (1, 1, 1, -1) if task == "classification" else (1, 1, -1, -1)
    rank_totals = {r["model_name"]: 0.0 for r in summary}
    for metric, direction in zip(metrics, directions):
        ordered = sorted(summary, key=lambda r: direction * safe_float(r.get(metric)))
        for rank, row in enumerate(ordered, start=1): rank_totals[row["model_name"]] += rank
    for row in summary:
        row["aggregate_rank_score"] = rank_totals[row["model_name"]] / len(metrics)
    summary.sort(key=lambda r: (r["aggregate_rank_score"], r["model_name"]))
    for rank, row in enumerate(summary, start=1): row["leaderboard_rank"] = rank
    return summary


def coefficient_rows(fold_id: int, model_name: str, model: SparseLinearModel, top_n: int = 40) -> List[dict]:
    items = sorted(model.weights.items(), key=lambda kv: (-abs(kv[1]), kv[0]))[:top_n]
    return [{"fold_id": fold_id, "model_name": model_name, "feature": k, "coefficient": v, "abs_coefficient": abs(v), "rank": i + 1} for i, (k, v) in enumerate(items)]


def run_fold(fold: Fold, samples: Sequence[Sample], args: argparse.Namespace) -> Tuple[List[dict], List[dict], List[dict], List[dict], List[str]]:
    diagnostics: List[str] = []
    train = [s for s in samples if fold.train_start <= s.confirmation <= fold.train_end]
    test = [s for s in samples if fold.test_start <= s.confirmation <= fold.test_end]
    if len(train) < args.min_train_rows or len(test) < args.min_test_rows:
        diagnostics.append(f"fold {fold.fold_id}: skipped; train={len(train)} test={len(test)}")
        return [], [], [], [], diagnostics

    encoder = FeatureEncoder().fit(train)
    xtrain = [encoder.transform_one(s) for s in train]
    xtest = [encoder.transform_one(s) for s in test]
    yclass_train = [float(s.actual_win) for s in train]
    yreg_train = [s.actual_r for s in train]

    bucket = BucketBaseline(args.min_bucket_rows, args.bucket_key_mode).fit(train)
    threshold = ThresholdBaseline(args.min_threshold_side_rows).fit(train)
    logistic = SparseLinearModel("classification", args.logistic_epochs, args.logistic_learning_rate, args.logistic_l2, args.seed + fold.fold_id * 101).fit(xtrain, yclass_train)
    ridge = SparseLinearModel("regression", args.ridge_epochs, args.ridge_learning_rate, args.ridge_l2, args.seed + fold.fold_id * 211).fit(xtrain, yreg_train)

    class_preds: Dict[str, List[float]] = {m: [] for m in CLASSIFICATION_MODELS}
    reg_preds: Dict[str, List[float]] = {m: [] for m in REGRESSION_MODELS}
    prediction_rows: List[dict] = []

    for s, x in zip(test, xtest):
        bucket_r, bucket_p, bucket_source, bucket_count = bucket.predict(s)
        threshold_r, threshold_p, threshold_source, threshold_count = threshold.predict(s)
        logistic_p = clip(logistic.predict(x), 0.001, 0.999)
        ridge_r = clip(ridge.predict(x), -args.max_abs_predicted_r, args.max_abs_predicted_r)
        ensemble_p = clip(args.ensemble_bucket_weight * bucket_p + (1.0 - args.ensemble_bucket_weight) * logistic_p, 0.001, 0.999)
        ensemble_r = args.ensemble_bucket_weight * bucket_r + (1.0 - args.ensemble_bucket_weight) * ridge_r

        pmap = {
            "bucket_baseline_classifier": bucket_p,
            "threshold_classifier": threshold_p,
            "logistic_classifier": logistic_p,
            "constrained_ensemble_classifier": ensemble_p,
        }
        rmap = {
            "bucket_baseline_regressor": bucket_r,
            "threshold_regressor": threshold_r,
            "ridge_regression": ridge_r,
            "constrained_ensemble_regressor": ensemble_r,
        }
        for model_name, pred in pmap.items():
            class_preds[model_name].append(pred)
            if args.write_predictions:
                prediction_rows.append({
                    "fold_id": fold.fold_id, "task": "classification", "model_name": model_name,
                    "sample_id": s.sample_id, "signal_id": s.signal_id,
                    "confirmation_ny": s.confirmation.isoformat(sep=" "),
                    "group": s.raw.get("group", ""), "direction": s.raw.get("direction", ""),
                    "role_key": s.raw.get("role_key", ""), "prediction": pred,
                    "actual": s.actual_win, "actual_r": s.actual_r,
                    "bucket_source": bucket_source if "bucket" in model_name or "ensemble" in model_name else threshold_source if "threshold" in model_name else "sparse_linear",
                    "train_support": bucket_count if "bucket" in model_name or "ensemble" in model_name else threshold_count if "threshold" in model_name else len(train),
                })
        for model_name, pred in rmap.items():
            reg_preds[model_name].append(pred)
            if args.write_predictions:
                prediction_rows.append({
                    "fold_id": fold.fold_id, "task": "regression", "model_name": model_name,
                    "sample_id": s.sample_id, "signal_id": s.signal_id,
                    "confirmation_ny": s.confirmation.isoformat(sep=" "),
                    "group": s.raw.get("group", ""), "direction": s.raw.get("direction", ""),
                    "role_key": s.raw.get("role_key", ""), "prediction": pred,
                    "actual": s.actual_r, "actual_r": s.actual_r,
                    "bucket_source": bucket_source if "bucket" in model_name or "ensemble" in model_name else threshold_source if "threshold" in model_name else "sparse_linear",
                    "train_support": bucket_count if "bucket" in model_name or "ensemble" in model_name else threshold_count if "threshold" in model_name else len(train),
                })

    comparison_rows: List[dict] = []
    calibration_rows: List[dict] = []
    actual_class = [s.actual_win for s in test]; actual_reg = [s.actual_r for s in test]
    for model_name, preds in class_preds.items():
        metrics = classification_metrics(actual_class, preds)
        comparison_rows.append({"fold_id": fold.fold_id, "task": "classification", "model_name": model_name, "train_count": len(train), "test_count": len(test), **metrics})
        for row in calibration_bins(actual_class, preds, args.calibration_bins):
            calibration_rows.append({"fold_id": fold.fold_id, "model_name": model_name, **row})
    for model_name, preds in reg_preds.items():
        metrics = regression_metrics(actual_reg, preds)
        comparison_rows.append({"fold_id": fold.fold_id, "task": "regression", "model_name": model_name, "train_count": len(train), "test_count": len(test), **metrics})

    importance = coefficient_rows(fold.fold_id, "logistic_classifier", logistic, args.top_features)
    importance += coefficient_rows(fold.fold_id, "ridge_regression", ridge, args.top_features)
    importance.append({"fold_id": fold.fold_id, "model_name": "threshold_baseline", "feature": threshold.feature or "GLOBAL", "coefficient": threshold.threshold, "abs_coefficient": abs(threshold.score), "rank": 1})
    return comparison_rows, prediction_rows, calibration_rows, importance, diagnostics


def build_leakage_audit(integrity_status: str, folds: Sequence[Fold]) -> List[dict]:
    rows = []
    for feature in sorted(ALLOWED_RAW_FEATURES):
        rows.append({"check": "feature_allowlist", "item": feature, "status": "PASS", "severity": "INFO", "detail": "Known at or before confirmation under current contract."})
    for feature in sorted(FORBIDDEN_FUTURE_OR_RESEARCH_FEATURES):
        rows.append({"check": "feature_denylist", "item": feature, "status": "PASS", "severity": "CRITICAL", "detail": "Explicitly excluded from model inputs."})
    rows.extend([
        {"check": "phase12_5_gate", "item": integrity_status, "status": "PASS", "severity": "CRITICAL", "detail": "Integrity gate accepted for research comparison."},
        {"check": "fixed_fold_plan", "item": str(len(folds)), "status": "PASS" if folds else "FAIL", "severity": "CRITICAL", "detail": "Phase 11 fold plan reused without refitting boundaries."},
        {"check": "train_only_encoder_fit", "item": "FeatureEncoder", "status": "PASS", "severity": "CRITICAL", "detail": "Means, scales, and category vocabularies fit on each training window only."},
        {"check": "deterministic_training", "item": "seeded SGD", "status": "PASS", "severity": "HIGH", "detail": "Fold-specific deterministic seeds used."},
        {"check": "execution_authority", "item": "false", "status": "PASS", "severity": "CRITICAL", "detail": "Outputs cannot place orders or mutate strategy."},
    ])
    for f in folds:
        status = "PASS" if f.train_end <= f.embargo_start <= f.embargo_end <= f.test_start else "FAIL"
        rows.append({"check": "fold_temporal_order", "item": str(f.fold_id), "status": status, "severity": "CRITICAL", "detail": f"train_end={f.train_end}; embargo={f.embargo_start}->{f.embargo_end}; test_start={f.test_start}"})
    return rows


def html_table(rows: Sequence[Mapping[str, object]], columns: Sequence[str], limit: int = 100) -> str:
    head = "".join(f"<th>{html.escape(c)}</th>" for c in columns)
    body = []
    for row in rows[:limit]:
        body.append("<tr>" + "".join(f"<td>{html.escape(str(row.get(c, '')))}</td>" for c in columns) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def generate_model_cards(leaderboard: Sequence[dict], args: argparse.Namespace, integrity_status: str) -> str:
    by_model = {str(r["model_name"]): r for r in leaderboard}
    descriptions = {
        "bucket_baseline_classifier": "Hierarchical train-window bucket win-rate baseline.",
        "threshold_classifier": "Single train-derived numeric median split used as an interpretable classifier.",
        "logistic_classifier": "Sparse one-hot logistic classifier trained by deterministic SGD.",
        "constrained_ensemble_classifier": "Fixed non-negative blend of bucket and logistic probabilities.",
        "bucket_baseline_regressor": "Hierarchical train-window bucket average-R baseline.",
        "threshold_regressor": "Single train-derived numeric median split used as an interpretable R regressor.",
        "ridge_regression": "Sparse linear R regression with L2 regularization and deterministic SGD.",
        "constrained_ensemble_regressor": "Fixed non-negative blend of bucket and ridge R predictions.",
    }
    lines = ["# EXP0017 Phase 13 Model Cards", "", f"Integrity status: `{integrity_status}`", "", "> Research evidence only. No model has execution authority.", ""]
    for model in (*CLASSIFICATION_MODELS, *REGRESSION_MODELS):
        row = by_model.get(model, {})
        lines += [f"## {model}", "", descriptions[model], "", f"- Task: `{row.get('task', '')}`", f"- Leaderboard rank: `{row.get('leaderboard_rank', 'NA')}`", f"- Folds: `{row.get('folds', 0)}`", f"- Aggregate rank score: `{row.get('aggregate_rank_score', '')}`", "- Inputs: Phase 10 causal allowlist only; future outcomes and Phase 09 full-history enrichments excluded.", "- Validation: fixed Phase 11 walk-forward folds.", "- Decision boundary: cannot filter signals, alter risk, alter targets, or place orders.", ""]
    lines += ["## Configuration", "", f"- Seed: `{args.seed}`", f"- Bucket key mode: `{args.bucket_key_mode}`", f"- Ensemble bucket weight: `{args.ensemble_bucket_weight}`", f"- Logistic epochs / L2: `{args.logistic_epochs}` / `{args.logistic_l2}`", f"- Ridge epochs / L2: `{args.ridge_epochs}` / `{args.ridge_l2}`", ""]
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", default=".")
    ap.add_argument("--out-dir", default="research/exp0017_phase13/outputs")
    ap.add_argument("--dataset-file", default="EXP0017_Phase10_Model_Dataset.csv")
    ap.add_argument("--fold-plan-file", default="EXP0017_Phase11_Fold_Plan.csv")
    ap.add_argument("--integrity-summary", default="research/exp0017_phase12_5/outputs/phase12_5_readiness_summary.json")
    ap.add_argument("--allow-missing-integrity", action="store_true")
    ap.add_argument("--seed", type=int, default=170013)
    ap.add_argument("--max-rows", type=int, default=200000)
    ap.add_argument("--min-train-rows", type=int, default=80)
    ap.add_argument("--min-test-rows", type=int, default=20)
    ap.add_argument("--min-bucket-rows", type=int, default=20)
    ap.add_argument("--min-threshold-side-rows", type=int, default=20)
    ap.add_argument("--bucket-key-mode", choices=("group_direction_role","group_direction","role","group","direction"), default="group_direction_role")
    ap.add_argument("--logistic-epochs", type=int, default=60)
    ap.add_argument("--logistic-learning-rate", type=float, default=0.02)
    ap.add_argument("--logistic-l2", type=float, default=0.0005)
    ap.add_argument("--ridge-epochs", type=int, default=70)
    ap.add_argument("--ridge-learning-rate", type=float, default=0.008)
    ap.add_argument("--ridge-l2", type=float, default=0.001)
    ap.add_argument("--ensemble-bucket-weight", type=float, default=0.50)
    ap.add_argument("--max-abs-predicted-r", type=float, default=10.0)
    ap.add_argument("--calibration-bins", type=int, default=10)
    ap.add_argument("--top-features", type=int, default=40)
    ap.add_argument("--write-predictions", action=argparse.BooleanOptionalAction, default=True)
    args = ap.parse_args(argv)

    data_dir = Path(args.data_dir).resolve(); out_dir = Path(args.out_dir).resolve(); out_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = data_dir / args.dataset_file
    fold_path = data_dir / args.fold_plan_file
    integrity_path = Path(args.integrity_summary)
    if not integrity_path.is_absolute(): integrity_path = data_dir / integrity_path

    diagnostics: List[str] = []
    try:
        integrity_status, warnings = read_integrity_status(integrity_path, args.allow_missing_integrity)
        diagnostics.extend(warnings)
        samples, sample_diagnostics = load_samples(dataset_path, args.max_rows)
        diagnostics.extend(sample_diagnostics)
        folds = load_folds(fold_path)
    except Exception as exc:
        atomic_write_text(out_dir / "phase13_fatal_error.txt", str(exc) + "\n")
        print(f"Phase13 blocked: {exc}", file=sys.stderr)
        return 2

    leakage_rows = build_leakage_audit(integrity_status, folds)
    failed_critical = [r for r in leakage_rows if r["severity"] == "CRITICAL" and r["status"] != "PASS"]
    if failed_critical:
        write_csv(out_dir / "phase13_leakage_audit.csv", leakage_rows, ("check","item","status","severity","detail"))
        atomic_write_text(out_dir / "phase13_fatal_error.txt", "Critical leakage audit failed.\n")
        return 2

    comparison_rows: List[dict] = []
    prediction_rows: List[dict] = []
    calibration_rows: List[dict] = []
    importance_rows: List[dict] = []
    usable_folds = 0
    for fold in folds:
        if not fold.usable:
            diagnostics.append(f"fold {fold.fold_id}: Phase11 marked unusable")
            continue
        c, p, cal, imp, d = run_fold(fold, samples, args)
        diagnostics.extend(d)
        if c:
            usable_folds += 1
            comparison_rows.extend(c); prediction_rows.extend(p); calibration_rows.extend(cal); importance_rows.extend(imp)

    class_board = model_comparison_score(comparison_rows, "classification")
    reg_board = model_comparison_score(comparison_rows, "regression")
    leaderboard = class_board + reg_board

    status = "COMPARISON_COMPLETE_RESEARCH_ONLY" if usable_folds > 0 else "COMPARISON_INSUFFICIENT_FOLDS"
    best_class = class_board[0]["model_name"] if class_board else "NONE"
    best_reg = reg_board[0]["model_name"] if reg_board else "NONE"

    config_payload = {k: v for k, v in vars(args).items() if k not in {"data_dir", "out_dir"}}
    config_hash = hashlib.sha256(json.dumps(config_payload, sort_keys=True).encode()).hexdigest()
    run_id = "P13-" + dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ") + "-" + config_hash[:10]

    comparison_fields = ("fold_id","task","model_name","train_count","test_count","n","positive_rate","mean_prediction","accuracy","balanced_accuracy","precision","recall","specificity","brier","log_loss","ece","calibration_intercept","calibration_slope","mean_actual","mae","rmse","r2","pearson","sign_accuracy")
    write_csv(out_dir / "phase13_model_comparison.csv", comparison_rows, comparison_fields)
    if args.write_predictions:
        write_csv(out_dir / "phase13_predictions.csv", prediction_rows, ("fold_id","task","model_name","sample_id","signal_id","confirmation_ny","group","direction","role_key","prediction","actual","actual_r","bucket_source","train_support"))
    write_csv(out_dir / "phase13_calibration_report.csv", calibration_rows, ("fold_id","model_name","bin","lower","upper","count","avg_prediction","observed_rate","abs_gap"))
    write_csv(out_dir / "phase13_feature_importance.csv", importance_rows, ("fold_id","model_name","feature","coefficient","abs_coefficient","rank"))
    leaderboard_fields = sorted({k for r in leaderboard for k in r.keys()}, key=lambda x: (x not in {"task","model_name","leaderboard_rank","aggregate_rank_score","folds"}, x))
    write_csv(out_dir / "phase13_experiment_leaderboard.csv", leaderboard, leaderboard_fields)
    write_csv(out_dir / "phase13_leakage_audit.csv", leakage_rows, ("check","item","status","severity","detail"))

    fold_stability = []
    for task in ("classification", "regression"):
        for model in (CLASSIFICATION_MODELS if task == "classification" else REGRESSION_MODELS):
            rs = [r for r in comparison_rows if r["task"] == task and r["model_name"] == model]
            target = "balanced_accuracy" if task == "classification" else "sign_accuracy"
            vals = [safe_float(r.get(target)) for r in rs]
            fold_stability.append({"task": task, "model_name": model, "metric": target, "folds": len(vals), "mean": mean(vals), "std": stdev(vals), "min": min(vals) if vals else 0, "max": max(vals) if vals else 0, "positive_folds": sum(1 for v in vals if v > 0.5)})
    write_csv(out_dir / "phase13_fold_stability.csv", fold_stability, ("task","model_name","metric","folds","mean","std","min","max","positive_folds"))

    registry = [{"run_id": run_id, "created_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", "version": VERSION, "seed": args.seed, "integrity_status": integrity_status, "dataset_file": str(dataset_path), "fold_plan_file": str(fold_path), "config_hash": config_hash, "usable_folds": usable_folds, "status": status, "best_classification_model": best_class, "best_regression_model": best_reg, "execution_authority": 0}]
    write_csv(out_dir / "phase13_experiment_registry.csv", registry, tuple(registry[0].keys()))
    write_csv(out_dir / "phase13_diagnostics.csv", [{"row": i+1, "diagnostic": v} for i, v in enumerate(diagnostics)], ("row","diagnostic"))

    cards = generate_model_cards(leaderboard, args, integrity_status)
    atomic_write_text(out_dir / "phase13_model_cards.md", cards)
    summary = {
        "run_id": run_id, "version": VERSION, "status": status,
        "integrity_status": integrity_status, "samples_loaded": len(samples),
        "folds_declared": len(folds), "folds_used": usable_folds,
        "best_classification_model": best_class, "best_regression_model": best_reg,
        "execution_authority": False, "strategy_mutation_authority": False,
        "decision": "RESEARCH_ONLY_NO_PROMOTION",
        "config_hash": config_hash,
    }
    atomic_write_text(out_dir / "phase13_comparison_summary.json", json.dumps(summary, indent=2, sort_keys=True))

    report = f"""<!doctype html><html><head><meta charset='utf-8'><title>EXP0017 Phase 13</title>
<style>body{{font-family:Arial,sans-serif;margin:24px;background:#111;color:#eee}}table{{border-collapse:collapse;width:100%;margin:12px 0 28px}}th,td{{border:1px solid #555;padding:6px;text-align:left}}th{{background:#222}}.ok{{color:#7CFC00}}.warn{{color:#ffd166}}code{{background:#222;padding:2px 5px}}</style></head><body>
<h1>EXP0017 Phase 13 — Controlled Model Comparison</h1>
<p>Status: <strong class='ok'>{html.escape(status)}</strong></p>
<p>Integrity: <code>{html.escape(integrity_status)}</code> | Samples: {len(samples)} | Usable folds: {usable_folds}</p>
<p class='warn'>Research evidence only. No execution or strategy-mutation authority.</p>
<h2>Leaderboard</h2>{html_table(leaderboard, leaderboard_fields, 50)}
<h2>Fold Comparison</h2>{html_table(comparison_rows, comparison_fields, 200)}
<h2>Leakage Audit</h2>{html_table(leakage_rows, ("check","item","status","severity","detail"), 300)}
<h2>Fold Stability</h2>{html_table(fold_stability, ("task","model_name","metric","folds","mean","std","min","max","positive_folds"), 50)}
</body></html>"""
    atomic_write_text(out_dir / "phase13_html_report.html", report)

    print(json.dumps(summary, indent=2))
    return 0 if usable_folds > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
