from __future__ import annotations
from typing import Any
from .canonical import content_hash


def _event(sequence: int, state: str, time_ms: int, quantity_fraction: float, reason: str, previous_hash: str) -> dict[str, Any]:
    payload = {"sequence": sequence, "state": state, "time_ms": time_ms, "quantity_fraction": round(quantity_fraction, 12), "reason": reason, "previous_event_hash": previous_hash}
    payload["event_hash"] = content_hash(payload)
    return payload


def build_lifecycle(decision_time_ms: int, action_class: str, status: str, fill_fraction: float, latency, maximum_events: int) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    previous = "0" * 64
    def append(state: str, delta_ms: int, fraction: float, reason: str) -> None:
        nonlocal previous
        if len(events) >= maximum_events:
            raise ValueError("lifecycle event budget exceeded")
        event = _event(len(events), state, decision_time_ms + delta_ms, fraction, reason, previous)
        events.append(event); previous = event["event_hash"]
    append("registered", 0, 0.0, "source_outcome_registered")
    if action_class in {"skip", "abstain"}:
        append("non_order", 0, 0.0, action_class)
        return events
    append("submitted", latency.submit_ms, 0.0, "deterministic_submit")
    if status in {"rejected", "broker_infeasible"}:
        append("rejected", latency.submit_ms + latency.acknowledgement_ms, 0.0, status)
        return events
    append("acknowledged", latency.submit_ms + latency.acknowledgement_ms, 0.0, "broker_acknowledgement")
    fill_time = latency.total_to_fill_ms
    if fill_fraction <= 0:
        append("expired", fill_time + latency.cancel_ms, 0.0, "deterministic_non_fill")
    elif fill_fraction < 1:
        append("partially_filled", fill_time, fill_fraction, "bounded_partial_fill")
        append("cancel_requested", fill_time, fill_fraction, "remainder_cancel")
        append("cancelled", fill_time + latency.cancel_ms, fill_fraction, "remainder_cancelled")
    else:
        append("filled", fill_time, 1.0, "deterministic_full_fill")
        append("exit_submitted", fill_time, 1.0, "source_exit_projection")
        append("closed", fill_time + latency.fill_ms, 1.0, "source_exit_projection")
    return events
