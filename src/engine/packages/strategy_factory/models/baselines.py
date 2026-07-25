"""Transparent baseline models with no external ML dependency."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional, Sequence

import numpy as np
import pandas as pd


class ModelError(RuntimeError):
    pass


@dataclass
class NumericStandardizer:
    mean_: Optional[np.ndarray] = None
    scale_: Optional[np.ndarray] = None

    def fit(self, x: np.ndarray) -> "NumericStandardizer":
        arr = np.asarray(x, dtype=float)
        self.mean_ = np.nanmean(arr, axis=0)
        scale = np.nanstd(arr, axis=0)
        scale[scale == 0] = 1.0
        self.scale_ = scale
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.scale_ is None:
            raise ModelError("standardizer is not fitted")
        arr = np.asarray(x, dtype=float)
        arr = np.where(np.isnan(arr), self.mean_, arr)
        return (arr - self.mean_) / self.scale_


@dataclass
class RidgeRegressor:
    alpha: float = 1.0
    coef_: Optional[np.ndarray] = None
    intercept_: float = 0.0
    standardizer_: NumericStandardizer = field(default_factory=NumericStandardizer)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "RidgeRegressor":
        x_std = self.standardizer_.fit(x).transform(x)
        target = np.asarray(y, dtype=float)
        self.intercept_ = float(np.mean(target))
        centered = target - self.intercept_
        design = np.column_stack([np.ones(len(x_std)), x_std])
        penalty = np.eye(design.shape[1]) * self.alpha
        penalty[0, 0] = 0.0
        beta = np.linalg.pinv(design.T @ design + penalty) @ design.T @ centered
        self.intercept_ += float(beta[0])
        self.coef_ = beta[1:]
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise ModelError("model is not fitted")
        return self.intercept_ + self.standardizer_.transform(x) @ self.coef_


@dataclass
class LogisticRegressionGD:
    learning_rate: float = 0.05
    iterations: int = 1500
    l2: float = 0.1
    coef_: Optional[np.ndarray] = None
    intercept_: float = 0.0
    standardizer_: NumericStandardizer = field(default_factory=NumericStandardizer)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "LogisticRegressionGD":
        x_std = self.standardizer_.fit(x).transform(x)
        target = np.asarray(y, dtype=float)
        if not set(np.unique(target)).issubset({0.0, 1.0}):
            raise ModelError("logistic target must be binary")
        n, p = x_std.shape
        coef = np.zeros(p, dtype=float)
        base_rate = np.clip(np.mean(target), 1e-6, 1 - 1e-6)
        intercept = float(np.log(base_rate / (1.0 - base_rate)))
        for _ in range(self.iterations):
            logits = np.clip(intercept + x_std @ coef, -30.0, 30.0)
            probs = 1.0 / (1.0 + np.exp(-logits))
            error = probs - target
            grad_coef = x_std.T @ error / n + self.l2 * coef
            grad_intercept = float(np.mean(error))
            coef -= self.learning_rate * grad_coef
            intercept -= self.learning_rate * grad_intercept
        self.coef_ = coef
        self.intercept_ = intercept
        return self

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise ModelError("model is not fitted")
        logits = np.clip(self.intercept_ + self.standardizer_.transform(x) @ self.coef_, -30.0, 30.0)
        positive = 1.0 / (1.0 + np.exp(-logits))
        return np.column_stack([1.0 - positive, positive])

    def predict(self, x: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(x)[:, 1] >= threshold).astype(int)


@dataclass
class ConstantBaseline:
    value: float = 0.0

    def fit(self, x: np.ndarray, y: np.ndarray) -> "ConstantBaseline":
        self.value = float(np.mean(y))
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.full(len(x), self.value, dtype=float)


@dataclass
class ThresholdRule:
    feature_index: int
    threshold: float
    direction: str = "greater"

    def predict(self, x: np.ndarray) -> np.ndarray:
        values = np.asarray(x, dtype=float)[:, self.feature_index]
        if self.direction == "greater":
            return (values >= self.threshold).astype(int)
        if self.direction == "less":
            return (values <= self.threshold).astype(int)
        raise ModelError("direction must be greater or less")


def numeric_matrix(frame: pd.DataFrame, feature_columns: Sequence[str]) -> np.ndarray:
    missing = [name for name in feature_columns if name not in frame.columns]
    if missing:
        raise KeyError(f"missing feature columns: {missing}")
    return frame[list(feature_columns)].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
