from __future__ import annotations
from dataclasses import dataclass
from .canonical import deterministic_unit_interval
from .models import ExecutionTwinProfile, Scenario

@dataclass(frozen=True)
class LatencyRealization:
    submit_ms: int
    acknowledgement_ms: int
    fill_ms: int
    cancel_ms: int
    jitter_ms: int
    total_to_fill_ms: int


def realize_latency(row_hash: str, scenario: Scenario, profile: ExecutionTwinProfile) -> LatencyRealization:
    signed = 2.0 * deterministic_unit_interval(row_hash, scenario.scenario_id, "latency") - 1.0
    jitter = int(round(signed * profile.latency.jitter_ms * scenario.latency_multiplier))
    submit = max(0, int(round(profile.latency.submit_ms * scenario.latency_multiplier)))
    ack = max(0, int(round(profile.latency.acknowledgement_ms * scenario.latency_multiplier)))
    fill = max(0, int(round(profile.latency.fill_ms * scenario.latency_multiplier + jitter)))
    cancel = max(0, int(round(profile.latency.cancel_ms * scenario.latency_multiplier)))
    return LatencyRealization(submit, ack, fill, cancel, jitter, submit + ack + fill)
