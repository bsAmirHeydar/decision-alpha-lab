"""Anatomy adapter protocol and shared adapter utilities."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterable, Mapping, Sequence

from ..contracts import AnatomyEvent, FeatureSnapshot
from ..manifest import StrategyManifest


class AnatomyAdapter(ABC):
    """Converts a domain anatomy into canonical events and immutable features.

    Adapters are not allowed to simulate outcomes, choose trades, allocate risk,
    or access future bars.  Their authority ends at event and feature creation.
    """

    adapter_id: str
    adapter_version: str

    @abstractmethod
    def emit_events(self, source: Any, manifest: StrategyManifest) -> Iterable[AnatomyEvent]:
        raise NotImplementedError

    @abstractmethod
    def build_snapshot(
        self,
        event: AnatomyEvent,
        source: Any,
        manifest: StrategyManifest,
        decision_time_utc: datetime,
    ) -> FeatureSnapshot:
        raise NotImplementedError

    def validate_event_set(self, events: Sequence[AnatomyEvent]) -> None:
        ids: set[str] = set()
        for event in events:
            event.validate()
            if event.event_id in ids:
                raise ValueError(f"duplicate event_id emitted by adapter: {event.event_id}")
            ids.add(event.event_id)

    def metadata(self) -> Mapping[str, str]:
        return {"adapter_id": self.adapter_id, "adapter_version": self.adapter_version}
