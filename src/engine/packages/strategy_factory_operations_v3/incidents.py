from __future__ import annotations

from dataclasses import replace

from .contracts import OperationsIncident
from .enums import IncidentSeverity, IncidentState
from .errors import OperationsError


def open_incident(
    incident_id: str,
    severity: IncidentSeverity,
    detected_at_ms: int,
    environment_hash: str,
    generation_hash: str,
    reason_code: str,
    evidence_hashes: tuple[str, ...],
    owner_id: str,
) -> OperationsIncident:
    return OperationsIncident(
        incident_id=incident_id,
        severity=severity,
        state=IncidentState.OPEN,
        detected_at_ms=detected_at_ms,
        contained_at_ms=0,
        resolved_at_ms=0,
        closed_at_ms=0,
        environment_hash=environment_hash,
        generation_hash=generation_hash,
        reason_code=reason_code,
        evidence_hashes=evidence_hashes,
        owner_id=owner_id,
    )


def contain_incident(incident: OperationsIncident, contained_at_ms: int, evidence_hash: str) -> OperationsIncident:
    if incident.state is not IncidentState.OPEN or contained_at_ms < incident.detected_at_ms:
        raise OperationsError("incident_transition", "only an open incident may be contained")
    return replace(incident, state=IncidentState.CONTAINED, contained_at_ms=contained_at_ms, evidence_hashes=incident.evidence_hashes + (evidence_hash,))


def resolve_incident(incident: OperationsIncident, resolved_at_ms: int, evidence_hash: str) -> OperationsIncident:
    if incident.state is not IncidentState.CONTAINED or resolved_at_ms < incident.contained_at_ms:
        raise OperationsError("incident_transition", "only a contained incident may be resolved")
    return replace(incident, state=IncidentState.RESOLVED, resolved_at_ms=resolved_at_ms, evidence_hashes=incident.evidence_hashes + (evidence_hash,))


def close_incident(incident: OperationsIncident, closed_at_ms: int, closed_by: str, evidence_hash: str) -> OperationsIncident:
    if incident.state is not IncidentState.RESOLVED or closed_at_ms < incident.resolved_at_ms:
        raise OperationsError("incident_transition", "only a resolved incident may be closed")
    if closed_by == incident.owner_id:
        raise OperationsError("incident_sod", "incident owner cannot self-close")
    return replace(incident, state=IncidentState.CLOSED, closed_at_ms=closed_at_ms, closed_by=closed_by, evidence_hashes=incident.evidence_hashes + (evidence_hash,))
