"""Deterministic boundary-case generators without an external property library."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterator

from ..contracts import AnatomyEvent, Direction


def event_cases() -> Iterator[AnatomyEvent]:
    base = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    for index, direction in enumerate((Direction.LONG, Direction.SHORT)):
        reference = 100.0 + index
        invalidation = reference - 1.0 if direction == Direction.LONG else reference + 1.0
        yield AnatomyEvent(
            event_id=f"case_{index}",
            strategy_id="test",
            strategy_version="1",
            symbol="TEST",
            direction=direction,
            event_time_utc=base,
            known_time_utc=base + timedelta(seconds=1),
            confirmation_time_utc=base + timedelta(seconds=2),
            reference_price=reference,
            invalidation_price=invalidation,
            market_event_cluster_id=f"cluster_{index}",
        )
