from __future__ import annotations
import math
from .models import ExecutionTwinProfile, Scenario
from .latency import LatencyRealization
from .queue import QueueRealization


def fill_probability(source_spread_points: float, scenario: Scenario, profile: ExecutionTwinProfile, latency: LatencyRealization, queue: QueueRealization) -> float:
    h = profile.fill_hazard
    spread_penalty = h.spread_sensitivity * max(0.0, source_spread_points * scenario.spread_multiplier)
    queue_penalty = h.queue_sensitivity * queue.queue_ahead_units
    latency_penalty = h.latency_sensitivity * (latency.total_to_fill_ms / 1000.0)
    probability = h.base_probability * math.exp(-(spread_penalty + queue_penalty + latency_penalty))
    return round(min(1.0, max(h.minimum_probability, probability)), 12)
