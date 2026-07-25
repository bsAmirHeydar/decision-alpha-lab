from __future__ import annotations
from .models import ExecutionTwinProfile
from .latency import LatencyRealization


def adverse_selection_points(fill_probability: float, latency: LatencyRealization, profile: ExecutionTwinProfile) -> float:
    p = profile.adverse_selection
    value = p.base_points + p.latency_coefficient * (latency.total_to_fill_ms / 1000.0) + p.non_fill_coefficient * (1.0 - fill_probability)
    return round(value, 12)
