from __future__ import annotations

import math
from statistics import median
from typing import Iterable, Sequence


def finite(value: float, label: str = "value") -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{label} must be finite")
    return value


def mean(values: Iterable[float]) -> float:
    data = [finite(value) for value in values]
    if not data:
        raise ValueError("mean requires at least one value")
    return sum(data) / len(data)


def variance(values: Iterable[float], ddof: int = 0) -> float:
    data = [finite(value) for value in values]
    if len(data) <= ddof:
        return 0.0
    center = mean(data)
    return sum((value - center) ** 2 for value in data) / (len(data) - ddof)


def standard_deviation(values: Iterable[float], ddof: int = 0) -> float:
    return math.sqrt(max(0.0, variance(values, ddof=ddof)))


def quantile(values: Sequence[float], probability: float) -> float:
    data = sorted(finite(value) for value in values)
    if not data:
        raise ValueError("quantile requires at least one value")
    probability = min(1.0, max(0.0, finite(probability, "probability")))
    index = probability * (len(data) - 1)
    left = int(math.floor(index))
    right = int(math.ceil(index))
    if left == right:
        return data[left]
    fraction = index - left
    return data[left] * (1.0 - fraction) + data[right] * fraction


def robust_center_scale(values: Sequence[float], floor: float = 1e-9) -> tuple[float, float]:
    data = [finite(value) for value in values]
    if not data:
        raise ValueError("robust center requires data")
    center = float(median(data))
    deviations = [abs(value - center) for value in data]
    scale = max(float(median(deviations)) * 1.4826, floor)
    return center, scale


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("dot dimension mismatch")
    return sum(finite(a) * finite(b) for a, b in zip(left, right))


def l2_distance(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("distance dimension mismatch")
    return math.sqrt(sum((finite(a) - finite(b)) ** 2 for a, b in zip(left, right)))


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    denominator = math.sqrt(dot(left, left) * dot(right, right))
    if denominator <= 1e-15:
        return 0.0
    return max(-1.0, min(1.0, dot(left, right) / denominator))


def clamp(value: float, lower: float, upper: float) -> float:
    if lower > upper:
        raise ValueError("invalid clamp bounds")
    return max(lower, min(upper, finite(value)))


def weighted_mean(vectors: Sequence[Sequence[float]], weights: Sequence[float]) -> list[float]:
    if not vectors or len(vectors) != len(weights):
        raise ValueError("weighted mean requires aligned non-empty inputs")
    dimension = len(vectors[0])
    if any(len(vector) != dimension for vector in vectors):
        raise ValueError("vector dimension mismatch")
    safe_weights = [max(0.0, finite(weight)) for weight in weights]
    total = sum(safe_weights)
    if total <= 0:
        raise ValueError("all weights are zero")
    return [sum(vector[index] * weight for vector, weight in zip(vectors, safe_weights)) / total for index in range(dimension)]
