"""Fail-closed multi-view fusion and view-ablation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import FusionPrediction
from .enums import FusionKind, MissingViewPolicy
from .errors import DeepViewError
from .math_utils import mean, ridge_fit, ridge_predict, variance


def _normalize(weights: Mapping[str, float]) -> dict[str, float]:
    positive = {key: max(0.0, float(value)) for key, value in weights.items()}
    total = sum(positive.values())
    if total <= 0:
        return {key: 1.0 / len(positive) for key in positive} if positive else {}
    return {key: value / total for key, value in positive.items()}


def _aligned_predictions(
    predictions: Mapping[str, Sequence[float | None]],
    targets: Sequence[float],
) -> None:
    if not predictions:
        raise DeepViewError("empty_fusion_views", "at least one fusion view is required")
    for view, values in predictions.items():
        if len(values) != len(targets):
            raise DeepViewError(
                "fusion_prediction_width_mismatch",
                "view prediction count differs from targets",
                {"view": view},
            )


@dataclass(frozen=True, slots=True)
class LateWeightedFusion:
    view_weights: Mapping[str, float]
    missing_policy: MissingViewPolicy
    global_fallback: float = 0.0

    @classmethod
    def fit(
        cls,
        predictions: Mapping[str, Sequence[float | None]],
        targets: Sequence[float],
        missing_policy: MissingViewPolicy = MissingViewPolicy.ABSTAIN,
    ) -> "LateWeightedFusion":
        _aligned_predictions(predictions, targets)
        weights: dict[str, float] = {}
        for view, values in predictions.items():
            pairs = [(float(value), float(target)) for value, target in zip(values, targets) if value is not None]
            if len(pairs) < 2:
                weights[view] = 0.0
                continue
            mse = mean((value - target) ** 2 for value, target in pairs)
            weights[view] = 1.0 / max(1e-12, mse)
        return cls(_normalize(weights), missing_policy, mean(targets))

    def predict(
        self,
        row_id: str,
        values: Mapping[str, float | None],
        uncertainties: Mapping[str, float] | None = None,
    ) -> FusionPrediction:
        uncertainties = uncertainties or {}
        available = {
            key: float(values[key])
            for key in self.view_weights
            if key in values and values[key] is not None
        }
        missing = tuple(sorted(set(self.view_weights) - set(available)))
        if missing and self.missing_policy is MissingViewPolicy.REJECT:
            raise DeepViewError(
                "missing_fusion_view",
                "required fusion view is missing",
                {"missing": missing},
            )
        if not available or (missing and self.missing_policy is MissingViewPolicy.ABSTAIN):
            fallback = self.missing_policy is MissingViewPolicy.GLOBAL_FALLBACK
            fused_value = self.global_fallback if fallback else 0.0
            abstained = not fallback
            reason = "global_fallback" if fallback else "missing_view"
            weights: dict[str, float] = {}
        else:
            weights = _normalize({key: self.view_weights.get(key, 0.0) for key in available})
            if not weights:
                raise DeepViewError("zero_fusion_reliability", "available views have zero fitted reliability")
            fused_value = sum(weights[key] * available[key] for key in weights)
            abstained = False
            reason = "fused"
        uncertainty = 0.0
        if weights:
            declared = sum(weights[key] * max(0.0, float(uncertainties.get(key, 0.0))) for key in weights)
            disagreement = variance(available[key] for key in weights) ** 0.5
            uncertainty = declared + disagreement
        material = {
            "row_id": row_id,
            "available": available,
            "missing": missing,
            "weights": weights,
            "value": fused_value,
            "uncertainty": uncertainty,
            "abstained": abstained,
            "reason": reason,
        }
        return FusionPrediction(
            prediction_id=stable_id("ucefusion", material),
            row_id=row_id,
            fusion_kind=FusionKind.LATE_WEIGHTED,
            available_views=tuple(sorted(available)),
            missing_views=missing,
            view_weights=weights,
            value=fused_value,
            uncertainty=uncertainty,
            abstained=abstained,
            reason=reason,
            evidence_hash=canonical_sha256(material),
        )


@dataclass(frozen=True, slots=True)
class GatedFusion:
    """Deterministic confidence gate over precomputed view predictions."""

    base_weights: Mapping[str, float]
    missing_policy: MissingViewPolicy
    minimum_total_confidence: float
    state_hash: str

    @classmethod
    def fit(
        cls,
        validation_predictions: Mapping[str, Sequence[float | None]],
        targets: Sequence[float],
        missing_policy: MissingViewPolicy = MissingViewPolicy.ABSTAIN,
        minimum_total_confidence: float = 0.1,
    ) -> "GatedFusion":
        late = LateWeightedFusion.fit(validation_predictions, targets, missing_policy)
        material = {
            "base_weights": dict(late.view_weights),
            "missing_policy": missing_policy.value,
            "minimum_total_confidence": minimum_total_confidence,
        }
        return cls(late.view_weights, missing_policy, float(minimum_total_confidence), canonical_sha256(material))

    def predict(
        self,
        row_id: str,
        values: Mapping[str, float | None],
        confidences: Mapping[str, float],
    ) -> FusionPrediction:
        available = {
            key: float(values[key])
            for key in self.base_weights
            if values.get(key) is not None
        }
        missing = tuple(sorted(set(self.base_weights) - set(available)))
        if missing and self.missing_policy is MissingViewPolicy.REJECT:
            raise DeepViewError("missing_gated_view", "required gated-fusion view is missing", {"missing": missing})
        if missing and self.missing_policy is MissingViewPolicy.ABSTAIN:
            weights: dict[str, float] = {}
        else:
            weights = _normalize(
                {
                    key: self.base_weights[key] * max(0.0, min(1.0, float(confidences.get(key, 0.0))))
                    for key in available
                }
            )
        total_confidence = sum(max(0.0, min(1.0, float(confidences.get(key, 0.0)))) for key in available)
        abstained = not weights or total_confidence < self.minimum_total_confidence
        value = 0.0 if abstained else sum(weights[key] * available[key] for key in weights)
        uncertainty = 1.0 if abstained else variance(available[key] for key in weights) ** 0.5
        reason = "insufficient_gate_confidence" if abstained else "gated_fusion"
        material = {
            "row_id": row_id,
            "available": available,
            "missing": missing,
            "weights": weights,
            "confidences": dict(confidences),
            "value": value,
            "abstained": abstained,
        }
        return FusionPrediction(
            stable_id("ucefusion", material),
            row_id,
            FusionKind.GATED,
            tuple(sorted(available)),
            missing,
            weights,
            value,
            uncertainty,
            abstained,
            reason,
            canonical_sha256(material),
        )


@dataclass(frozen=True, slots=True)
class StackedFusion:
    view_order: tuple[str, ...]
    coefficients: tuple[float, ...]
    missing_policy: MissingViewPolicy
    state_hash: str

    @classmethod
    def fit(
        cls,
        predictions: Mapping[str, Sequence[float | None]],
        targets: Sequence[float],
        alpha: float = 1e-3,
        missing_policy: MissingViewPolicy = MissingViewPolicy.ZERO_FILL,
        oof_predictions: bool = True,
    ) -> "StackedFusion":
        if not oof_predictions:
            raise DeepViewError(
                "stacking_requires_oof_predictions",
                "stacking may only fit from out-of-fold base predictions",
            )
        _aligned_predictions(predictions, targets)
        order = tuple(sorted(predictions))
        rows = [
            tuple(float(predictions[key][index]) if predictions[key][index] is not None else 0.0 for key in order)
            for index in range(len(targets))
        ]
        coefficients = ridge_fit(rows, targets, alpha)
        material = {
            "view_order": order,
            "coefficients": coefficients,
            "missing_policy": missing_policy.value,
            "oof_predictions": True,
        }
        return cls(order, coefficients, missing_policy, canonical_sha256(material))

    def predict(self, row_id: str, values: Mapping[str, float | None]) -> FusionPrediction:
        missing = tuple(key for key in self.view_order if values.get(key) is None)
        if missing and self.missing_policy is MissingViewPolicy.REJECT:
            raise DeepViewError("missing_stacking_view", "stacking view is missing", {"missing": missing})
        if missing and self.missing_policy is MissingViewPolicy.ABSTAIN:
            material = {"row_id": row_id, "missing": missing, "abstained": True}
            return FusionPrediction(
                stable_id("ucefusion", material),
                row_id,
                FusionKind.STACKED,
                tuple(key for key in self.view_order if key not in missing),
                missing,
                {},
                0.0,
                0.0,
                True,
                "missing_view",
                canonical_sha256(material),
            )
        row = tuple(float(values.get(key) or 0.0) for key in self.view_order)
        value = ridge_predict(self.coefficients, row)
        weights = {key: 1.0 / len(self.view_order) for key in self.view_order}
        material = {"row_id": row_id, "view_order": self.view_order, "row": row, "value": value}
        return FusionPrediction(
            stable_id("ucefusion", material),
            row_id,
            FusionKind.STACKED,
            tuple(key for key in self.view_order if key not in missing),
            missing,
            weights,
            value,
            0.0,
            False,
            "stacked",
            canonical_sha256(material),
        )


def ablation_increment(
    full_predictions: Sequence[float],
    ablated_predictions: Sequence[float],
    targets: Sequence[float],
    maximize: bool = True,
) -> float:
    if not (len(full_predictions) == len(ablated_predictions) == len(targets)):
        raise DeepViewError("ablation_width_mismatch", "ablation arrays must have equal width")

    def negative_mse(predictions: Sequence[float]) -> float:
        return -mean((float(prediction) - float(target)) ** 2 for prediction, target in zip(predictions, targets))

    full_metric = negative_mse(full_predictions)
    ablated_metric = negative_mse(ablated_predictions)
    return full_metric - ablated_metric if maximize else ablated_metric - full_metric
