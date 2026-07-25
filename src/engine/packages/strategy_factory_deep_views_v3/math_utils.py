"""Small deterministic numeric primitives used by native UCE-I10 references.

The native floor deliberately avoids NumPy so conformance can run in the base
installation and can be mirrored in MQL5. These routines are not intended to
replace optimized scientific libraries for admitted optional adapters.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence

from .errors import DeepViewError


def _finite(value: float, name: str = "value") -> float:
    result = float(value)
    if not math.isfinite(result):
        raise DeepViewError("non_finite_numeric_value", f"{name} must be finite")
    return result


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise DeepViewError(
            "dot_width_mismatch",
            "dot-product operands must have equal width",
            {"left": len(a), "right": len(b)},
        )
    return sum(_finite(x) * _finite(y) for x, y in zip(a, b))


def mean(values: Iterable[float]) -> float:
    material = [_finite(value) for value in values]
    return sum(material) / len(material) if material else 0.0


def variance(values: Iterable[float], sample: bool = False) -> float:
    material = [_finite(value) for value in values]
    if not material:
        return 0.0
    if sample and len(material) < 2:
        return 0.0
    center = sum(material) / len(material)
    denominator = len(material) - 1 if sample else len(material)
    return sum((value - center) ** 2 for value in material) / denominator


def std(values: Iterable[float], sample: bool = False) -> float:
    return math.sqrt(max(0.0, variance(values, sample=sample)))


def sigmoid(value: float) -> float:
    value = _finite(value)
    if value >= 0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


def softmax(values: Sequence[float], temperature: float = 1.0) -> tuple[float, ...]:
    if temperature <= 0:
        raise DeepViewError("invalid_softmax_temperature", "temperature must be positive")
    if not values:
        return ()
    scaled = [_finite(value) / temperature for value in values]
    maximum = max(scaled)
    exponents = [math.exp(value - maximum) for value in scaled]
    total = sum(exponents)
    return tuple(value / total for value in exponents)


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    if len(actual) != len(predicted):
        raise DeepViewError("metric_width_mismatch", "metric inputs must have equal width")
    return mean(abs(_finite(a) - _finite(b)) for a, b in zip(actual, predicted))


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    if len(actual) != len(predicted):
        raise DeepViewError("metric_width_mismatch", "metric inputs must have equal width")
    return math.sqrt(mean((_finite(a) - _finite(b)) ** 2 for a, b in zip(actual, predicted)))


def percentile(values: Sequence[float], quantile: float) -> float:
    if not 0.0 <= quantile <= 1.0:
        raise DeepViewError("invalid_quantile", "quantile must be in [0,1]")
    material = sorted(_finite(value) for value in values)
    if not material:
        return 0.0
    position = (len(material) - 1) * quantile
    lower = int(position)
    upper = min(len(material) - 1, lower + 1)
    weight = position - lower
    return material[lower] * (1.0 - weight) + material[upper] * weight


def solve_linear(matrix: Sequence[Sequence[float]], rhs: Sequence[float]) -> tuple[float, ...]:
    """Solve a square system with deterministic pivot tie-breaking.

    Singular pivots are retained as zero coefficients. This is acceptable for
    the reference ridge floor because regularized feature dimensions should be
    non-singular; the behavior remains explicit and deterministic if they are not.
    """

    size = len(rhs)
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise DeepViewError("linear_system_shape_mismatch", "matrix must be square and match rhs")
    augmented = [
        [_finite(value) for value in row] + [_finite(rhs[index])]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: (abs(augmented[row][column]), -row))
        if abs(augmented[pivot][column]) < 1e-12:
            continue
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor != 0.0:
                augmented[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[column])
                ]
    return tuple(
        augmented[index][-1] if abs(augmented[index][index]) >= 1e-12 else 0.0
        for index in range(size)
    )


def ridge_fit(
    rows: Sequence[Sequence[float]],
    targets: Sequence[float],
    alpha: float = 1e-3,
    weights: Sequence[float] | None = None,
) -> tuple[float, ...]:
    if alpha < 0:
        raise DeepViewError("negative_ridge_alpha", "ridge alpha cannot be negative")
    if len(rows) != len(targets):
        raise DeepViewError("ridge_row_target_mismatch", "row and target counts differ")
    if not rows:
        return ()
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise DeepViewError("ridge_feature_width_mismatch", "ridge rows have different widths")
    if weights is None:
        normalized_weights = [1.0] * len(rows)
    else:
        if len(weights) != len(rows):
            raise DeepViewError("ridge_weight_width_mismatch", "weight count differs from rows")
        normalized_weights = [_finite(value, "sample_weight") for value in weights]
        if any(value <= 0 for value in normalized_weights):
            raise DeepViewError("invalid_ridge_weight", "ridge sample weights must be positive")

    design = [tuple(_finite(value) for value in row) + (1.0,) for row in rows]
    response = [_finite(value) for value in targets]
    parameter_count = width + 1
    gram = [[0.0] * parameter_count for _ in range(parameter_count)]
    cross = [0.0] * parameter_count
    for row, target, weight in zip(design, response, normalized_weights):
        for left in range(parameter_count):
            cross[left] += weight * row[left] * target
            for right in range(parameter_count):
                gram[left][right] += weight * row[left] * row[right]
    for index in range(parameter_count - 1):
        gram[index][index] += alpha
    return solve_linear(gram, cross)


def ridge_predict(coefficients: Sequence[float], row: Sequence[float]) -> float:
    if not coefficients:
        return 0.0
    if len(coefficients) != len(row) + 1:
        raise DeepViewError(
            "ridge_prediction_width_mismatch",
            "coefficient width must equal feature width plus intercept",
        )
    return dot(coefficients[:-1], row) + _finite(coefficients[-1])
