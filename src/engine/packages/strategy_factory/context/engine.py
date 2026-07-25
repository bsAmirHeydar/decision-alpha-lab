"""Incremental, dependency-aware online context engine."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

from ..contracts import AnatomyEvent, FeatureSnapshot, FeatureValue, stable_hash
from ..plugins.interfaces import FeatureProvider
from .cache import BoundedTTLCache
from .graph import CompiledFeatureGraph


class ContextBuildError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ContextBuildResult:
    snapshot: FeatureSnapshot
    flat: Mapping[str, Any]
    cache_hits: int
    cache_misses: int
    missing_required: tuple[str, ...]


class IncrementalContextEngine:
    """Build immutable context snapshots while recomputing only dirty providers.

    Cache keys include strategy/event identity and a caller-provided market-state
    generation. A generation should change whenever an input used by the
    provider changes. This avoids expensive deep hashing on the live path.
    """

    __slots__ = ("graph", "cache", "schema_version", "producer_version")

    def __init__(
        self,
        graph: CompiledFeatureGraph,
        *,
        cache: BoundedTTLCache | None = None,
        schema_version: str = "2.0.0",
        producer_version: str = "2.0.0",
    ) -> None:
        self.graph = graph
        self.cache = cache or BoundedTTLCache()
        self.schema_version = schema_version
        self.producer_version = producer_version

    def build(
        self,
        event: AnatomyEvent,
        market_state: Mapping[str, Any],
        decision_time_utc: datetime,
        *,
        state_generation: int = 0,
        base_context: Mapping[str, Any] | None = None,
    ) -> ContextBuildResult:
        event.validate()
        resolved: dict[str, Any] = dict(base_context or {})
        features: list[FeatureValue] = []
        hits = 0
        misses = 0

        for provider in self.graph.ordered_providers:
            descriptor = provider.descriptor
            cache_key = (
                event.strategy_id,
                event.event_id,
                descriptor.plugin_id,
                descriptor.version,
                state_generation,
            )
            cached = self.cache.get(cache_key)
            if cached is not None and cached.version == descriptor.version:
                produced = cached.value
                hits += 1
            else:
                produced = tuple(provider.compute(event, resolved, market_state, decision_time_utc))
                for item in produced:
                    item.validate(decision_time_utc)
                self.cache.put(
                    cache_key,
                    produced,
                    ttl_seconds=provider.ttl_seconds,
                    version=descriptor.version,
                )
                misses += 1
            for item in produced:
                resolved[item.name] = item.value
                features.append(item)

        missing = tuple(sorted(name for name in self.graph.required_features if name not in resolved or resolved.get(name) is None))
        payload = {
            "event_id": event.event_id,
            "decision_time": decision_time_utc.isoformat(),
            "schema_version": self.schema_version,
            "producer_version": self.producer_version,
            "features": [(item.name, item.value, item.version) for item in features],
        }
        snapshot = FeatureSnapshot(
            snapshot_id=stable_hash(payload, prefix="snap_")[:40],
            event_id=event.event_id,
            snapshot_time_utc=decision_time_utc,
            features=tuple(features),
            schema_version=self.schema_version,
            producer_version=self.producer_version,
        )
        snapshot.validate()
        return ContextBuildResult(snapshot, resolved, hits, misses, missing)
