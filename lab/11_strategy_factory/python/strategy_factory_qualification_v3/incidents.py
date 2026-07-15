from __future__ import annotations
from typing import Iterable, Tuple
from .contracts import IncidentRecord
from .enums import IncidentSeverity


def open_critical_incidents(incidents: Iterable[IncidentRecord], as_of_ms: int) -> Tuple[IncidentRecord, ...]:
    return tuple(sorted((item for item in incidents if item.severity is IncidentSeverity.CRITICAL and item.closed_at_ms > as_of_ms), key=lambda x: x.incident_id))


def incident_gate_reasons(incidents: Iterable[IncidentRecord]) -> Tuple[str, ...]:
    reasons = []
    for item in incidents:
        if item.severity is IncidentSeverity.CRITICAL:
            reasons.append(f"critical_incident:{item.incident_id}")
        elif not item.root_cause or not item.corrective_action:
            reasons.append(f"incomplete_incident_record:{item.incident_id}")
    return tuple(sorted(set(reasons)))
