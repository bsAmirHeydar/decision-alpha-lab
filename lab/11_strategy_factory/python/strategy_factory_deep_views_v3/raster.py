"""Deterministic chart raster construction and native vision reference floor."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import PixelAuditReport, RasterArtifact, RasterSpec
from .errors import DeepViewError
from .math_utils import mean, ridge_fit, ridge_predict, sigmoid, std


def _validate_candle(candle: Mapping[str, float | int]) -> dict[str, float | int]:
    required = ("time_ms", "open", "high", "low", "close")
    missing = [field for field in required if field not in candle]
    if missing:
        raise DeepViewError("raster_candle_field_missing", "candle is missing required fields", {"fields": missing})
    normalized = {
        "time_ms": int(candle["time_ms"]),
        "open": float(candle["open"]),
        "high": float(candle["high"]),
        "low": float(candle["low"]),
        "close": float(candle["close"]),
        "volume": float(candle.get("volume", 0.0)),
    }
    if any(not math.isfinite(float(normalized[field])) for field in ("open", "high", "low", "close", "volume")):
        raise DeepViewError("non_finite_ohlc", "OHLCV values must be finite")
    if normalized["high"] < max(normalized["open"], normalized["close"], normalized["low"]):
        raise DeepViewError("invalid_ohlc", "high is below candle values")
    if normalized["low"] > min(normalized["open"], normalized["close"], normalized["high"]):
        raise DeepViewError("invalid_ohlc", "low is above candle values")
    if normalized["volume"] < 0:
        raise DeepViewError("negative_volume", "volume cannot be negative")
    return normalized


def _price_bounds(spec: RasterSpec, candles: Sequence[Mapping[str, float | int]]) -> tuple[float, float]:
    lows = [float(candle["low"]) for candle in candles]
    highs = [float(candle["high"]) for candle in candles]
    if spec.price_normalization == "window_min_max":
        lower, upper = min(lows), max(highs)
    else:
        center = float(candles[-1]["close"])
        half_range = max(max(highs) - min(lows), 1e-12) / 2.0
        lower, upper = center - half_range, center + half_range
    if upper <= lower:
        upper = lower + 1.0
    return lower, upper


def _row_for_price(price: float, lower: float, upper: float, height: int) -> int:
    ratio = (float(price) - lower) / (upper - lower)
    return max(0, min(height - 1, height - 1 - int(round(ratio * (height - 1)))))


def render_chart_raster(
    spec: RasterSpec,
    context_observation_id: str,
    known_time_ms: int,
    candles: Sequence[Mapping[str, float | int]],
) -> RasterArtifact:
    if not context_observation_id:
        raise DeepViewError("context_id_required", "context_observation_id is required")
    # Future rows are excluded before any ordering or duplicate validation.
    # A malformed/unordered future suffix must not alter a past artifact.
    eligible = [
        _validate_candle(candle)
        for candle in candles
        if int(candle["time_ms"]) <= int(known_time_ms)
    ]
    eligible.sort(key=lambda candle: int(candle["time_ms"]))
    times = [int(candle["time_ms"]) for candle in eligible]
    if any(left >= right for left, right in zip(times, times[1:])):
        raise DeepViewError("raster_time_not_strict", "known-time raster source times must strictly increase")
    selected = eligible[-spec.width :]
    if not selected:
        raise DeepViewError("empty_raster_source", "no known-time candles are available")

    lower, upper = _price_bounds(spec, selected)
    channel_count = len(spec.channels)
    grid = [0.0] * (channel_count * spec.height * spec.width)

    def put(channel: int, row: int, column: int, value: float, replace: bool = False) -> None:
        index = (channel * spec.height + row) * spec.width + column
        grid[index] = float(value) if replace else max(grid[index], float(value))

    channel_index = {name: index for index, name in enumerate(spec.channels)}
    offset = spec.width - len(selected)
    maximum_volume = max(float(candle["volume"]) for candle in selected) or 1.0
    maximum_range = max(float(candle["high"]) - float(candle["low"]) for candle in selected) or 1.0

    for position, candle in enumerate(selected):
        column = offset + position
        open_price = float(candle["open"])
        high_price = float(candle["high"])
        low_price = float(candle["low"])
        close_price = float(candle["close"])
        open_row = _row_for_price(open_price, lower, upper, spec.height)
        close_row = _row_for_price(close_price, lower, upper, spec.height)
        high_row = _row_for_price(high_price, lower, upper, spec.height)
        low_row = _row_for_price(low_price, lower, upper, spec.height)

        if "wick" in channel_index:
            for row in range(min(high_row, low_row), max(high_row, low_row) + 1):
                put(channel_index["wick"], row, column, 1.0)
        if "body" in channel_index:
            for row in range(min(open_row, close_row), max(open_row, close_row) + 1):
                put(channel_index["body"], row, column, 1.0)
        if "direction" in channel_index:
            direction = 1.0 if close_price >= open_price else -1.0
            put(channel_index["direction"], close_row, column, direction, replace=True)
        if "close" in channel_index:
            put(channel_index["close"], close_row, column, 1.0)
        if "volume" in channel_index:
            value = float(candle["volume"]) / maximum_volume
            put(channel_index["volume"], spec.height - 1, column, value, replace=True)
        if "range" in channel_index:
            value = (high_price - low_price) / maximum_range
            put(channel_index["range"], spec.height - 1, column, value, replace=True)

    source_material = tuple(selected)
    source_hash = canonical_sha256(source_material)
    identity = {
        "spec_hash": spec.spec_hash,
        "context_observation_id": context_observation_id,
        "known_time_ms": int(known_time_ms),
        "source_hash": source_hash,
        "shape": (channel_count, spec.height, spec.width),
        "values": tuple(grid),
    }
    return RasterArtifact(
        artifact_id=stable_id("uceraster", identity),
        spec_hash=spec.spec_hash,
        context_observation_id=context_observation_id,
        known_time_ms=int(known_time_ms),
        shape=(channel_count, spec.height, spec.width),
        values=tuple(grid),
        source_hash=source_hash,
        evidence_hash=canonical_sha256(identity),
    )


def audit_prefix_invariance(
    spec: RasterSpec,
    context_observation_id: str,
    known_time_ms: int,
    candles: Sequence[Mapping[str, float | int]],
    future_candles: Sequence[Mapping[str, float | int]],
    tolerance: float = 0.0,
) -> PixelAuditReport:
    if tolerance < 0:
        raise DeepViewError("negative_pixel_tolerance", "pixel tolerance cannot be negative")
    first = render_chart_raster(spec, context_observation_id, known_time_ms, candles)
    second = render_chart_raster(
        spec,
        context_observation_id,
        known_time_ms,
        tuple(candles) + tuple(future_candles),
    )
    differences = [abs(left - right) for left, right in zip(first.values, second.values)]
    maximum = max(differences, default=0.0)
    changed = sum(value > tolerance for value in differences)
    material = {
        "artifact_a_hash": first.evidence_hash,
        "artifact_b_hash": second.evidence_hash,
        "max_abs_difference": maximum,
        "changed_pixel_count": changed,
        "tolerance": tolerance,
    }
    return PixelAuditReport(
        report_id=stable_id("ucepixelaudit", material),
        artifact_a_hash=first.evidence_hash,
        artifact_b_hash=second.evidence_hash,
        max_abs_difference=maximum,
        changed_pixel_count=changed,
        prefix_invariant=changed == 0,
        evidence_hash=canonical_sha256(material),
    )


def prefix_invariance_passes(
    spec: RasterSpec,
    context_observation_id: str,
    known_time_ms: int,
    candles: Sequence[Mapping[str, float | int]],
    future_candles: Sequence[Mapping[str, float | int]],
) -> bool:
    return audit_prefix_invariance(
        spec,
        context_observation_id,
        known_time_ms,
        candles,
        future_candles,
    ).prefix_invariant


class RasterConvEncoder:
    """Fixed local-gradient and pooled-statistic encoder for raster baselines."""

    def encode(self, values: Sequence[float], shape: tuple[int, int, int]) -> tuple[float, ...]:
        channels, height, width = map(int, shape)
        expected = channels * height * width
        if len(values) != expected:
            raise DeepViewError(
                "raster_width_mismatch",
                "raster payload width differs from shape",
                {"expected": expected, "actual": len(values)},
            )
        output: list[float] = []
        for channel in range(channels):
            base = channel * height * width
            plane = [float(value) for value in values[base : base + height * width]]
            if any(not math.isfinite(value) for value in plane):
                raise DeepViewError("non_finite_raster_value", "raster values must be finite")
            horizontal = [
                plane[row * width + column + 1] - plane[row * width + column]
                for row in range(height)
                for column in range(width - 1)
            ]
            vertical = [
                plane[(row + 1) * width + column] - plane[row * width + column]
                for row in range(height - 1)
                for column in range(width)
            ]
            top = plane[: max(1, (height // 2) * width)]
            bottom = plane[(height // 2) * width :]
            left = [plane[row * width + column] for row in range(height) for column in range(max(1, width // 2))]
            right = [plane[row * width + column] for row in range(height) for column in range(width // 2, width)]
            output.extend(
                (
                    mean(plane),
                    std(plane),
                    max(plane),
                    min(plane),
                    mean(horizontal),
                    std(horizontal),
                    mean(vertical),
                    std(vertical),
                    mean(top),
                    mean(bottom),
                    mean(left),
                    mean(right),
                )
            )
        return tuple(output)


@dataclass(frozen=True, slots=True)
class RasterConvModel:
    shape: tuple[int, int, int]
    coefficients: tuple[tuple[float, ...], ...]
    output_count: int
    probability_output: bool
    state_hash: str

    @classmethod
    def fit(
        cls,
        values: Sequence[Sequence[float]],
        targets: Sequence[Sequence[float]],
        shape: tuple[int, int, int],
        alpha: float = 1e-3,
        probability_output: bool = False,
        weights: Sequence[float] | None = None,
    ) -> "RasterConvModel":
        if len(values) != len(targets) or not values:
            raise DeepViewError("invalid_raster_training_set", "raster rows and targets must be non-empty and aligned")
        output_count = len(targets[0])
        if output_count < 1 or any(len(target) != output_count for target in targets):
            raise DeepViewError("raster_target_width_mismatch", "raster target widths differ")
        encoder = RasterConvEncoder()
        features = [encoder.encode(row, shape) for row in values]
        coefficients = tuple(
            ridge_fit(features, [target[index] for target in targets], alpha, weights)
            for index in range(output_count)
        )
        material = {
            "shape": tuple(shape),
            "coefficients": coefficients,
            "probability_output": probability_output,
        }
        return cls(tuple(shape), coefficients, output_count, probability_output, canonical_sha256(material))

    def predict(self, values: Sequence[float]) -> tuple[float, ...]:
        features = RasterConvEncoder().encode(values, self.shape)
        raw = tuple(ridge_predict(coefficients, features) for coefficients in self.coefficients)
        return tuple(sigmoid(value) for value in raw) if self.probability_output else raw
