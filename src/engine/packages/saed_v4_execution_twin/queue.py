from __future__ import annotations
from dataclasses import dataclass
from .canonical import deterministic_unit_interval
from .models import ExecutionTwinProfile, Scenario

@dataclass(frozen=True)
class QueueRealization:
    queue_ahead_units: float
    participation_rate: float
    uncertainty_draw: float


def realize_queue(row_hash: str, scenario: Scenario, profile: ExecutionTwinProfile) -> QueueRealization:
    draw = 2.0 * deterministic_unit_interval(row_hash, scenario.scenario_id, "queue") - 1.0
    queue = max(0.0, profile.queue.base_queue_units * scenario.queue_multiplier + draw * profile.queue.uncertainty_units)
    return QueueRealization(round(queue, 10), profile.queue.participation_rate, round(draw, 10))
