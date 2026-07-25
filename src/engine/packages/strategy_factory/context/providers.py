"""Reusable feature-provider implementations."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Mapping, Sequence

from ..contracts import AnatomyEvent, FeatureValue
from ..plugins.interfaces import PluginDescriptor


ComputeFn = Callable[[AnatomyEvent, Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]


@dataclass(slots=True)
class MappingFeatureProvider:
    descriptor: PluginDescriptor
    feature_names: tuple[str, ...]
    compute_fn: ComputeFn
    dependencies: tuple[str, ...] = ()
    ttl_seconds: float | None = None
    required: bool = True

    def compute(
        self,
        event: AnatomyEvent,
        resolved: Mapping[str, Any],
        market_state: Mapping[str, Any],
        decision_time_utc: datetime,
    ) -> Sequence[FeatureValue]:
        raw = self.compute_fn(event, resolved, market_state)
        missing = [name for name in self.feature_names if name not in raw]
        if missing and self.required:
            raise KeyError(f"provider {self.descriptor.plugin_id} omitted required outputs {missing}")
        return tuple(
            FeatureValue(
                name=name,
                value=raw.get(name),
                known_time_utc=decision_time_utc,
                source=self.descriptor.plugin_id,
                version=self.descriptor.version,
                missing_reason=None if name in raw else "provider_missing_optional",
            )
            for name in self.feature_names
        )
