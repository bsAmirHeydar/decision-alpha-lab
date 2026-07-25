"""Fast local model implementations and model routing."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Mapping, Sequence

from ..plugins.interfaces import PluginDescriptor


@dataclass(frozen=True, slots=True)
class LinearModel:
    descriptor: PluginDescriptor
    feature_order: tuple[str, ...]
    coefficients: tuple[float, ...]
    intercept: float = 0.0
    output_name: str = "score"
    logistic: bool = False

    def __post_init__(self) -> None:
        if len(self.feature_order) != len(self.coefficients):
            raise ValueError("feature_order and coefficients must have equal length")

    def _predict(self, values: Sequence[float]) -> float:
        if len(values) != len(self.coefficients):
            raise ValueError("input vector length does not match coefficients")
        score = self.intercept + sum(c * float(v) for c, v in zip(self.coefficients, values))
        if self.logistic:
            if score >= 0:
                return 1.0 / (1.0 + exp(-score))
            ez = exp(score)
            return ez / (1.0 + ez)
        return float(score)

    def predict_one(self, values: Sequence[float]) -> Mapping[str, float]:
        return {self.output_name: self._predict(values)}

    def predict_batch(self, rows: Sequence[Sequence[float]]) -> Sequence[Mapping[str, float]]:
        return tuple({self.output_name: self._predict(row)} for row in rows)


@dataclass(frozen=True, slots=True)
class ModelRoute:
    model_id: str
    model_version: str
    feature_schema_id: str
    output_mapping: Mapping[str, str]
    required: bool = True


class ModelRouter:
    __slots__ = ("_models", "_routes")

    def __init__(self, models: Mapping[str, object], routes: Sequence[ModelRoute]) -> None:
        self._models = dict(models)
        self._routes = tuple(routes)

    def predict(
        self,
        vectors: Mapping[str, Sequence[float]],
    ) -> dict[str, Mapping[str, float]]:
        outputs: dict[str, Mapping[str, float]] = {}
        for route in self._routes:
            model = self._models.get(route.model_id)
            vector = vectors.get(route.feature_schema_id)
            if model is None or vector is None:
                if route.required:
                    missing = "model" if model is None else "feature_vector"
                    raise KeyError(f"missing required {missing} for route {route.model_id}")
                continue
            raw = model.predict_one(vector)
            outputs[route.model_id] = {
                target_name: float(raw[source_name])
                for target_name, source_name in route.output_mapping.items()
                if source_name in raw
            }
        return outputs
