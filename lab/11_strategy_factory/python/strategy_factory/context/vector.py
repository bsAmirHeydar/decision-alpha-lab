"""Low-allocation feature vectors for online inference."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
import math


class FeatureVectorError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FeatureVectorSchema:
    names: tuple[str, ...]
    defaults: tuple[float, ...]
    version: str

    def __post_init__(self) -> None:
        if len(self.names) != len(self.defaults):
            raise FeatureVectorError("names and defaults must have equal length")
        if len(set(self.names)) != len(self.names):
            raise FeatureVectorError("feature vector names must be unique")

    def encode(self, context: Mapping[str, Any], *, strict: bool = False) -> tuple[float, ...]:
        values: list[float] = []
        for name, default in zip(self.names, self.defaults):
            raw = context.get(name, default)
            if raw is None:
                if strict:
                    raise FeatureVectorError(f"missing required model feature: {name}")
                raw = default
            try:
                value = float(raw)
            except (TypeError, ValueError) as exc:
                raise FeatureVectorError(f"feature {name!r} cannot be converted to float: {raw!r}") from exc
            if not math.isfinite(value):
                raise FeatureVectorError(f"feature {name!r} is not finite")
            values.append(value)
        return tuple(values)

    def mapping(self, values: Sequence[float]) -> dict[str, float]:
        if len(values) != len(self.names):
            raise FeatureVectorError("vector length does not match schema")
        return dict(zip(self.names, map(float, values)))
