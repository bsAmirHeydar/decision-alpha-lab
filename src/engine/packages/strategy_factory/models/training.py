"""Shared walk-forward training, prediction, calibration, and candidate ranking."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence

import numpy as np
import pandas as pd

from .baselines import ConstantBaseline, LogisticRegressionGD, RidgeRegressor, numeric_matrix
from ..validation.folds import PurgedWalkForwardSplitter


@dataclass(frozen=True)
class FoldMetric:
    fold_id: int
    train_count: int
    test_count: int
    metric_name: str
    metric_value: float


@dataclass(frozen=True)
class TrainingResult:
    model_id: str
    task: str
    feature_columns: Sequence[str]
    target_column: str
    predictions: pd.DataFrame
    fold_metrics: Sequence[FoldMetric]
    metadata: Mapping[str, object]


def binary_log_loss(y_true: np.ndarray, probability: np.ndarray) -> float:
    p = np.clip(np.asarray(probability, dtype=float), 1e-12, 1 - 1e-12)
    y = np.asarray(y_true, dtype=float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def brier_score(y_true: np.ndarray, probability: np.ndarray) -> float:
    return float(np.mean((np.asarray(probability) - np.asarray(y_true)) ** 2))


def mean_squared_error(y_true: np.ndarray, prediction: np.ndarray) -> float:
    return float(np.mean((np.asarray(prediction) - np.asarray(y_true)) ** 2))


def calibration_table(y_true: Sequence[float], probability: Sequence[float], bins: int = 10) -> pd.DataFrame:
    frame = pd.DataFrame({"y": y_true, "p": probability}).dropna()
    if frame.empty:
        return pd.DataFrame(columns=["bin", "count", "mean_probability", "observed_rate"])
    frame["bin"] = pd.cut(frame["p"], bins=np.linspace(0, 1, bins + 1), include_lowest=True)
    result = (
        frame.groupby("bin", observed=False)
        .agg(count=("y", "size"), mean_probability=("p", "mean"), observed_rate=("y", "mean"))
        .reset_index()
    )
    result["bin"] = result["bin"].astype(str)
    return result


def train_walk_forward(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str],
    target_column: str,
    task: str,
    splitter: PurgedWalkForwardSplitter,
    model_factory: Optional[Callable[[], object]] = None,
    model_id: str = "shared_baseline",
    time_col: str = "known_time_utc",
    label_end_col: str = "label_end_time_utc",
    cluster_col: str = "market_event_cluster_id",
) -> TrainingResult:
    if target_column not in frame:
        raise KeyError(target_column)
    predictions = []
    metrics: List[FoldMetric] = []

    if task not in {"classification", "regression"}:
        raise ValueError("task must be classification or regression")
    if model_factory is None:
        model_factory = (lambda: LogisticRegressionGD()) if task == "classification" else (lambda: RidgeRegressor())

    for fold in splitter.split(
        frame,
        time_col=time_col,
        label_end_col=label_end_col,
        cluster_col=cluster_col if cluster_col in frame.columns else None,
    ):
        train = frame.iloc[fold.train_index]
        test = frame.iloc[fold.test_index]
        x_train = numeric_matrix(train, feature_columns)
        x_test = numeric_matrix(test, feature_columns)
        y_train = train[target_column].to_numpy(dtype=float)
        y_test = test[target_column].to_numpy(dtype=float)
        model = model_factory()
        model.fit(x_train, y_train)  # type: ignore[attr-defined]

        if task == "classification":
            probability = model.predict_proba(x_test)[:, 1]  # type: ignore[attr-defined]
            prediction = (probability >= 0.5).astype(int)
            metrics.extend(
                [
                    FoldMetric(fold.fold_id, len(train), len(test), "log_loss", binary_log_loss(y_test, probability)),
                    FoldMetric(fold.fold_id, len(train), len(test), "brier", brier_score(y_test, probability)),
                    FoldMetric(fold.fold_id, len(train), len(test), "accuracy", float(np.mean(prediction == y_test))),
                ]
            )
            score = probability
        else:
            score = model.predict(x_test)  # type: ignore[attr-defined]
            metrics.extend(
                [
                    FoldMetric(fold.fold_id, len(train), len(test), "mse", mean_squared_error(y_test, score)),
                    FoldMetric(fold.fold_id, len(train), len(test), "mean_prediction", float(np.mean(score))),
                ]
            )

        for position, source_index in enumerate(fold.test_index):
            row = {
                "source_index": int(source_index),
                "fold_id": fold.fold_id,
                "target": float(y_test[position]),
                "prediction": float(score[position]),
            }
            for identity in ("event_id", "candidate_id", cluster_col, time_col):
                if identity in frame.columns:
                    row[identity] = frame.iloc[source_index][identity]
            predictions.append(row)

    prediction_frame = pd.DataFrame(predictions).sort_values("source_index", kind="stable") if predictions else pd.DataFrame()
    return TrainingResult(
        model_id=model_id,
        task=task,
        feature_columns=tuple(feature_columns),
        target_column=target_column,
        predictions=prediction_frame,
        fold_metrics=tuple(metrics),
        metadata={"fold_count": len(set(prediction_frame.get("fold_id", []))) if not prediction_frame.empty else 0},
    )


def rank_candidates(
    frame: pd.DataFrame,
    *,
    score_col: str = "prediction",
    event_col: str = "event_id",
    minimum_score: Optional[float] = None,
) -> pd.DataFrame:
    result = frame.copy()
    result["candidate_rank"] = result.groupby(event_col)[score_col].rank(method="first", ascending=False)
    result["selected"] = result["candidate_rank"] == 1
    if minimum_score is not None:
        result["selected"] &= result[score_col] >= minimum_score
    return result
