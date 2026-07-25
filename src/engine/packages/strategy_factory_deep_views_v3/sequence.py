"""Causal sequence construction and deterministic temporal reference model."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import SequenceArtifact, SequenceWindowSpec
from .errors import DeepViewError
from .math_utils import mean, ridge_fit, ridge_predict, sigmoid, std


def unflatten_sequence(
    values: Sequence[float],
    shape: tuple[int, int],
    layout: str = "time_major",
) -> tuple[tuple[float, ...], ...]:
    steps, channels = int(shape[0]), int(shape[1])
    if steps < 1 or channels < 1:
        raise DeepViewError("invalid_sequence_shape", "sequence shape must be positive")
    if len(values) != steps * channels:
        raise DeepViewError(
            "sequence_width_mismatch",
            "sequence payload width differs from shape",
            {"expected": steps * channels, "actual": len(values)},
        )
    material = tuple(float(value) for value in values)
    if any(not math.isfinite(value) for value in material):
        raise DeepViewError("non_finite_sequence_value", "sequence values must be finite")
    if layout == "time_major":
        return tuple(
            tuple(material[step * channels + channel] for channel in range(channels))
            for step in range(steps)
        )
    if layout == "feature_major":
        return tuple(
            tuple(material[channel * steps + step] for channel in range(channels))
            for step in range(steps)
        )
    raise DeepViewError(
        "unsupported_sequence_layout",
        "layout must be time_major or feature_major",
        {"layout": layout},
    )


def flatten_sequence(
    rows: Sequence[Sequence[float]],
    layout: str = "time_major",
) -> tuple[float, ...]:
    if not rows:
        return ()
    channels = len(rows[0])
    if channels < 1 or any(len(row) != channels for row in rows):
        raise DeepViewError("sequence_row_width_mismatch", "sequence rows have different widths")
    if layout == "time_major":
        return tuple(float(value) for row in rows for value in row)
    if layout == "feature_major":
        return tuple(float(rows[step][channel]) for channel in range(channels) for step in range(len(rows)))
    raise DeepViewError("unsupported_sequence_layout", "layout must be time_major or feature_major")


def validate_causal_sequence(
    values: Sequence[float],
    shape: tuple[int, int],
    timestamps_ms: Sequence[int],
    known_time_ms: int,
    mask: Sequence[int] = (),
    layout: str = "time_major",
    require_zero_for_masked: bool = False,
) -> tuple[tuple[float, ...], ...]:
    rows = unflatten_sequence(values, shape, layout)
    if len(timestamps_ms) != len(rows):
        raise DeepViewError(
            "sequence_timestamp_width_mismatch",
            "one timestamp per sequence step is required",
        )
    timestamps = tuple(int(value) for value in timestamps_ms)
    if any(value > int(known_time_ms) for value in timestamps):
        raise DeepViewError("future_sequence_value", "sequence includes a future timestamp")
    if any(left >= right for left, right in zip(timestamps, timestamps[1:])):
        raise DeepViewError(
            "non_monotone_sequence_time",
            "sequence timestamps must strictly increase",
        )
    if mask:
        if len(mask) != len(values):
            raise DeepViewError("sequence_mask_width_mismatch", "sequence mask width differs")
        if any(value not in (0, 1) for value in mask):
            raise DeepViewError("invalid_sequence_mask", "sequence mask must be binary")
        if require_zero_for_masked:
            for value, present in zip(values, mask):
                if not present and float(value) != 0.0:
                    raise DeepViewError(
                        "non_zero_masked_sequence_value",
                        "masked sequence values must equal the declared pad value",
                    )
    return rows


class SequenceWindowBuilder:
    """Build a fixed-width left-padded sequence from known-time observations."""

    def __init__(self, spec: SequenceWindowSpec) -> None:
        self.spec = spec

    def build(
        self,
        context_observation_id: str,
        known_time_ms: int,
        observations: Sequence[Mapping[str, float | int]],
    ) -> SequenceArtifact:
        if not context_observation_id:
            raise DeepViewError("context_id_required", "context_observation_id is required")
        eligible = [
            observation
            for observation in observations
            if int(observation["time_ms"]) <= int(known_time_ms)
        ]
        eligible.sort(key=lambda observation: int(observation["time_ms"]))
        if self.spec.require_strict_time:
            times = [int(observation["time_ms"]) for observation in eligible]
            if any(left >= right for left, right in zip(times, times[1:])):
                raise DeepViewError(
                    "duplicate_or_reordered_sequence_source",
                    "source observations must have strictly increasing times",
                )
        selected = eligible[-self.spec.steps :]
        padding = self.spec.steps - len(selected)
        channels = len(self.spec.feature_order)
        rows: list[tuple[float, ...]] = [
            tuple(self.spec.pad_value for _ in range(channels))
            for _ in range(padding)
        ]
        mask_rows: list[tuple[int, ...]] = [tuple(0 for _ in range(channels)) for _ in range(padding)]
        if selected:
            first_time = int(selected[0]["time_ms"])
        else:
            first_time = int(known_time_ms)
        timestamps = [first_time - (padding - index) for index in range(padding)]
        for observation in selected:
            row = []
            row_mask = []
            for feature in self.spec.feature_order:
                raw = observation.get(feature)
                if raw is None:
                    row.append(self.spec.pad_value)
                    row_mask.append(0)
                else:
                    value = float(raw)
                    if not math.isfinite(value):
                        raise DeepViewError(
                            "non_finite_sequence_source",
                            "source sequence feature must be finite",
                            {"feature": feature},
                        )
                    row.append(value)
                    row_mask.append(1)
            rows.append(tuple(row))
            mask_rows.append(tuple(row_mask))
            timestamps.append(int(observation["time_ms"]))
        values = flatten_sequence(rows, self.spec.layout)
        mask = tuple(int(value) for value in flatten_sequence(mask_rows, self.spec.layout))
        validate_causal_sequence(
            values,
            self.spec.shape,
            timestamps,
            known_time_ms,
            mask,
            self.spec.layout,
            require_zero_for_masked=self.spec.pad_value == 0.0,
        )
        source_material = tuple(
            {
                "time_ms": int(observation["time_ms"]),
                **{feature: observation.get(feature) for feature in self.spec.feature_order},
            }
            for observation in selected
        )
        source_hash = canonical_sha256(source_material)
        identity = {
            "spec_hash": self.spec.spec_hash,
            "context_observation_id": context_observation_id,
            "known_time_ms": int(known_time_ms),
            "timestamps_ms": timestamps,
            "values": values,
            "mask": mask,
            "source_hash": source_hash,
        }
        return SequenceArtifact(
            artifact_id=stable_id("ucesequence", identity),
            spec_hash=self.spec.spec_hash,
            context_observation_id=context_observation_id,
            known_time_ms=int(known_time_ms),
            timestamps_ms=tuple(timestamps),
            values=values,
            mask=mask,
            source_hash=source_hash,
            evidence_hash=canonical_sha256(identity),
        )


class TemporalConvEncoder:
    """Deterministic causal convolution/summary encoder.

    It is the native baseline floor, not a claim that a learned neural TCN has
    been trained. Optional deep adapters must beat or match this reference under
    the same OOF protocol before they can qualify.
    """

    def __init__(
        self,
        kernel_sizes: Sequence[int] = (2, 3),
        dilations: Sequence[int] = (1, 2),
    ) -> None:
        self.kernel_sizes = tuple(int(value) for value in kernel_sizes)
        self.dilations = tuple(int(value) for value in dilations)
        if not self.kernel_sizes or any(value < 2 for value in self.kernel_sizes):
            raise DeepViewError("invalid_temporal_kernel", "kernel sizes must be >= 2")
        if not self.dilations or any(value < 1 for value in self.dilations):
            raise DeepViewError("invalid_temporal_dilation", "dilations must be positive")

    def encode(
        self,
        rows: Sequence[Sequence[float]],
        mask: Sequence[int] = (),
    ) -> tuple[float, ...]:
        if not rows:
            return ()
        steps = len(rows)
        channels = len(rows[0])
        if channels < 1 or any(len(row) != channels for row in rows):
            raise DeepViewError("sequence_row_width_mismatch", "sequence rows differ in width")
        valid = [[1] * channels for _ in range(steps)]
        if mask:
            if len(mask) != steps * channels:
                raise DeepViewError("sequence_mask_width_mismatch", "invalid mask width")
            if any(value not in (0, 1) for value in mask):
                raise DeepViewError("invalid_sequence_mask", "mask must be binary")
            valid = [
                [int(mask[step * channels + channel]) for channel in range(channels)]
                for step in range(steps)
            ]
        output: list[float] = []
        for channel in range(channels):
            observed = [
                float(rows[step][channel])
                for step in range(steps)
                if valid[step][channel]
            ]
            if not observed:
                output.extend((0.0, 0.0, 0.0, 0.0, 0.0))
            else:
                slope = (observed[-1] - observed[0]) / max(1, len(observed) - 1)
                output.extend(
                    (
                        observed[-1],
                        mean(observed),
                        std(observed),
                        slope,
                        len(observed) / steps,
                    )
                )
            for kernel_size in self.kernel_sizes:
                for dilation in self.dilations:
                    required = (kernel_size - 1) * dilation + 1
                    if steps < required:
                        output.append(0.0)
                        continue
                    indices = [steps - 1 - offset * dilation for offset in range(kernel_size)]
                    if not all(valid[index][channel] for index in indices):
                        output.append(0.0)
                        continue
                    samples = [float(rows[index][channel]) for index in indices]
                    if kernel_size == 2:
                        value = samples[0] - samples[1]
                    elif kernel_size == 3:
                        value = samples[0] - 2.0 * samples[1] + samples[2]
                    else:
                        # Higher-order kernels use a causal endpoint-minus-window-mean contrast.
                        value = samples[0] - mean(samples[1:])
                    output.append(value)
        return tuple(output)


@dataclass(frozen=True, slots=True)
class CausalTemporalConvModel:
    shape: tuple[int, int]
    layout: str
    kernel_sizes: tuple[int, ...]
    dilations: tuple[int, ...]
    coefficients: tuple[tuple[float, ...], ...]
    output_count: int
    probability_output: bool
    state_hash: str

    @classmethod
    def fit(
        cls,
        values: Sequence[Sequence[float]],
        targets: Sequence[Sequence[float]],
        shape: tuple[int, int],
        layout: str = "time_major",
        masks: Sequence[Sequence[int]] | None = None,
        alpha: float = 1e-3,
        probability_output: bool = False,
        weights: Sequence[float] | None = None,
        kernel_sizes: Sequence[int] = (2, 3),
        dilations: Sequence[int] = (1, 2),
    ) -> "CausalTemporalConvModel":
        if len(values) != len(targets):
            raise DeepViewError("sequence_target_count_mismatch", "sequence and target counts differ")
        if not values:
            raise DeepViewError("empty_sequence_training_set", "sequence training set cannot be empty")
        output_count = len(targets[0])
        if output_count < 1 or any(len(target) != output_count for target in targets):
            raise DeepViewError("sequence_target_width_mismatch", "target widths differ")
        normalized_masks = masks or [() for _ in values]
        if len(normalized_masks) != len(values):
            raise DeepViewError("sequence_mask_count_mismatch", "mask count differs from sequence count")
        encoder = TemporalConvEncoder(kernel_sizes, dilations)
        features = [
            encoder.encode(unflatten_sequence(row, shape, layout), mask)
            for row, mask in zip(values, normalized_masks)
        ]
        coefficients = tuple(
            ridge_fit(features, [target[index] for target in targets], alpha, weights)
            for index in range(output_count)
        )
        material = {
            "shape": tuple(shape),
            "layout": layout,
            "kernel_sizes": encoder.kernel_sizes,
            "dilations": encoder.dilations,
            "coefficients": coefficients,
            "probability_output": probability_output,
        }
        return cls(
            shape=tuple(shape),
            layout=layout,
            kernel_sizes=encoder.kernel_sizes,
            dilations=encoder.dilations,
            coefficients=coefficients,
            output_count=output_count,
            probability_output=probability_output,
            state_hash=canonical_sha256(material),
        )

    def encode(self, values: Sequence[float], mask: Sequence[int] = ()) -> tuple[float, ...]:
        return TemporalConvEncoder(self.kernel_sizes, self.dilations).encode(
            unflatten_sequence(values, self.shape, self.layout),
            mask,
        )

    def predict(self, values: Sequence[float], mask: Sequence[int] = ()) -> tuple[float, ...]:
        features = self.encode(values, mask)
        raw = tuple(ridge_predict(coefficients, features) for coefficients in self.coefficients)
        if self.probability_output:
            return tuple(sigmoid(value) for value in raw)
        return raw
