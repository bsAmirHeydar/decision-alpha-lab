"""Deterministic regime, change-point, novelty, and expert-gating primitives."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import RegimeNoveltyPrediction
from .enums import RegimeGateDecision
from .errors import DeepViewError
from .math_utils import mean, percentile, softmax, std


def _distance(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise DeepViewError("regime_width_mismatch", "regime vectors have different widths")
    return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(left, right)))


def _validate_rows(rows: Sequence[Sequence[float]], code: str) -> list[tuple[float, ...]]:
    material = [tuple(float(value) for value in row) for row in rows]
    if not material:
        raise DeepViewError(code, "training rows cannot be empty")
    width = len(material[0])
    if width < 1 or any(len(row) != width for row in material):
        raise DeepViewError("regime_width_mismatch", "feature widths differ")
    if any(not math.isfinite(value) for row in material for value in row):
        raise DeepViewError("non_finite_regime_value", "regime values must be finite")
    return material


@dataclass(frozen=True, slots=True)
class RegimeModel:
    """Deterministic K-means state model with transition evidence."""

    centroids: tuple[tuple[float, ...], ...]
    support: tuple[int, ...]
    transition_counts: tuple[tuple[int, ...], ...]
    state_hash: str

    @classmethod
    def fit(
        cls,
        rows: Sequence[Sequence[float]],
        k: int = 3,
        iterations: int = 50,
    ) -> "RegimeModel":
        material = _validate_rows(rows, "empty_regime_rows")
        if k < 1 or len(material) < k:
            raise DeepViewError("insufficient_regime_rows", "row count must be at least k")
        if iterations < 1:
            raise DeepViewError("invalid_regime_iterations", "iterations must be positive")
        width = len(material[0])

        # Quantile-spaced deterministic seeds avoid random initialization drift.
        ordered = sorted(material, key=lambda row: (row[0], row))
        centroids = [
            ordered[min(len(ordered) - 1, round(index * (len(ordered) - 1) / max(1, k - 1)))]
            for index in range(k)
        ]
        labels = [-1] * len(material)
        for _ in range(iterations):
            next_labels = [
                min(range(k), key=lambda index: (_distance(row, centroids[index]), index))
                for row in material
            ]
            next_centroids: list[tuple[float, ...]] = []
            for index in range(k):
                group = [row for row, label in zip(material, next_labels) if label == index]
                if group:
                    next_centroids.append(
                        tuple(mean(row[column] for row in group) for column in range(width))
                    )
                else:
                    next_centroids.append(centroids[index])
            if next_labels == labels and tuple(next_centroids) == tuple(centroids):
                break
            labels, centroids = next_labels, next_centroids

        # Canonical state IDs are ordered lexicographically by centroid, then old ID.
        order = sorted(range(k), key=lambda index: (tuple(centroids[index]), index))
        remap = {old: new for new, old in enumerate(order)}
        canonical_centroids = tuple(tuple(centroids[index]) for index in order)
        canonical_labels = [remap[label] for label in labels]
        support = tuple(canonical_labels.count(index) for index in range(k))
        transitions = [[0] * k for _ in range(k)]
        for left, right in zip(canonical_labels, canonical_labels[1:]):
            transitions[left][right] += 1
        transition_counts = tuple(tuple(row) for row in transitions)
        identity = {
            "centroids": canonical_centroids,
            "support": support,
            "transition_counts": transition_counts,
        }
        return cls(canonical_centroids, support, transition_counts, canonical_sha256(identity))

    def assign(self, row: Sequence[float]) -> tuple[int, float, tuple[float, ...]]:
        distances = tuple(_distance(row, centroid) for centroid in self.centroids)
        index = min(range(len(distances)), key=lambda position: (distances[position], position))
        probabilities = softmax(tuple(-distance for distance in distances))
        return index, probabilities[index], distances

    def transition_probabilities(self, regime_index: int, smoothing: float = 1.0) -> tuple[float, ...]:
        if regime_index < 0 or regime_index >= len(self.transition_counts):
            raise DeepViewError("regime_index_out_of_range", "regime index is out of range")
        if smoothing < 0:
            raise DeepViewError("negative_transition_smoothing", "smoothing cannot be negative")
        row = self.transition_counts[regime_index]
        denominator = sum(row) + smoothing * len(row)
        if denominator <= 0:
            return tuple(1.0 / len(row) for _ in row)
        return tuple((count + smoothing) / denominator for count in row)


@dataclass(frozen=True, slots=True)
class DistanceNoveltyModel:
    center: tuple[float, ...]
    scale: tuple[float, ...]
    threshold: float
    state_hash: str

    @classmethod
    def fit(
        cls,
        rows: Sequence[Sequence[float]],
        quantile: float = 0.95,
    ) -> "DistanceNoveltyModel":
        material = _validate_rows(rows, "empty_novelty_rows")
        if not 0.5 <= quantile < 1.0:
            raise DeepViewError("invalid_novelty_quantile", "novelty quantile must be in [0.5,1)")
        width = len(material[0])
        center = tuple(mean(row[column] for row in material) for column in range(width))
        scale = tuple(max(1e-9, std(row[column] for row in material)) for column in range(width))
        scores = [
            math.sqrt(
                sum(((row[column] - center[column]) / scale[column]) ** 2 for column in range(width))
            )
            for row in material
        ]
        threshold = percentile(scores, quantile)
        identity = {"center": center, "scale": scale, "threshold": threshold, "quantile": quantile}
        return cls(center, scale, threshold, canonical_sha256(identity))

    def score(self, row: Sequence[float]) -> float:
        if len(row) != len(self.center):
            raise DeepViewError("novelty_width_mismatch", "novelty row width differs from fitted state")
        return math.sqrt(
            sum(
                ((float(row[column]) - self.center[column]) / self.scale[column]) ** 2
                for column in range(len(self.center))
            )
        )


@dataclass(frozen=True, slots=True)
class CusumChangeDetector:
    reference_mean: float
    reference_std: float
    drift: float
    threshold: float

    @classmethod
    def fit(
        cls,
        values: Sequence[float],
        drift_sigma: float = 0.25,
        threshold_sigma: float = 4.0,
    ) -> "CusumChangeDetector":
        if not values:
            raise DeepViewError("empty_cusum_reference", "CUSUM reference values cannot be empty")
        if drift_sigma < 0 or threshold_sigma <= 0:
            raise DeepViewError("invalid_cusum_parameters", "CUSUM parameters are invalid")
        reference_mean = mean(values)
        reference_std = max(1e-9, std(values))
        return cls(
            reference_mean,
            reference_std,
            drift_sigma * reference_std,
            threshold_sigma * reference_std,
        )

    def score(self, values: Sequence[float]) -> float:
        positive = 0.0
        negative = 0.0
        maximum = 0.0
        for value in values:
            residual = float(value) - self.reference_mean
            positive = max(0.0, positive + residual - self.drift)
            negative = max(0.0, negative - residual - self.drift)
            maximum = max(maximum, positive, negative)
        return maximum / self.threshold

    def first_alarm_index(self, values: Sequence[float]) -> int | None:
        positive = 0.0
        negative = 0.0
        for index, value in enumerate(values):
            residual = float(value) - self.reference_mean
            positive = max(0.0, positive + residual - self.drift)
            negative = max(0.0, negative - residual - self.drift)
            if max(positive, negative) >= self.threshold:
                return index
        return None


class RegimeExpertGate:
    """Select a supported expert, global fallback, or fail-closed abstention."""

    def __init__(
        self,
        model: RegimeModel,
        novelty: DistanceNoveltyModel,
        expert_keys: Sequence[str],
        minimum_support: int = 10,
        minimum_probability: float = 0.55,
        novelty_abstain: float = 1.25,
        global_key: str = "global",
        change_abstain: float = 2.0,
    ) -> None:
        self.model = model
        self.novelty = novelty
        self.expert_keys = tuple(expert_keys)
        self.minimum_support = int(minimum_support)
        self.minimum_probability = float(minimum_probability)
        self.novelty_abstain = float(novelty_abstain)
        self.global_key = global_key
        self.change_abstain = float(change_abstain)
        if len(self.expert_keys) != len(model.centroids):
            raise DeepViewError("expert_regime_count_mismatch", "one expert key per regime is required")
        if self.minimum_support < 1:
            raise DeepViewError("invalid_minimum_regime_support", "minimum support must be positive")
        if not 0.0 <= self.minimum_probability <= 1.0:
            raise DeepViewError("invalid_regime_probability_gate", "minimum probability must be in [0,1]")

    def predict(
        self,
        row_id: str,
        row: Sequence[float],
        change_score: float = 0.0,
    ) -> RegimeNoveltyPrediction:
        regime_index, probability, _ = self.model.assign(row)
        novelty_score = self.novelty.score(row)
        support = self.model.support[regime_index]
        if change_score > self.change_abstain:
            decision = RegimeGateDecision.ABSTAIN
            expert_key = ""
            reason = "change_point_threshold_exceeded"
        elif novelty_score > self.novelty.threshold * self.novelty_abstain:
            decision = RegimeGateDecision.ABSTAIN
            expert_key = ""
            reason = "novelty_threshold_exceeded"
        elif support < self.minimum_support or probability < self.minimum_probability:
            decision = RegimeGateDecision.GLOBAL
            expert_key = self.global_key
            reason = "sparse_or_uncertain_regime"
        else:
            decision = RegimeGateDecision.EXPERT
            expert_key = self.expert_keys[regime_index]
            reason = "supported_regime"
        material = {
            "row_id": row_id,
            "regime_index": regime_index,
            "probability": probability,
            "novelty_score": novelty_score,
            "change_score": float(change_score),
            "support": support,
            "decision": decision.value,
            "expert_key": expert_key,
        }
        return RegimeNoveltyPrediction(
            prediction_id=stable_id("uceregime", material),
            row_id=row_id,
            regime_id=f"regime_{regime_index}",
            regime_probability=probability,
            novelty_score=novelty_score,
            change_score=float(change_score),
            support_count=support,
            decision=decision,
            expert_key=expert_key,
            reason=reason,
            evidence_hash=canonical_sha256(material),
        )
