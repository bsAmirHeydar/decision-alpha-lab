"""Constitutional incident qualification and mandatory response mapping."""
from __future__ import annotations

from dataclasses import dataclass


INCIDENT_RESPONSES = {
    "evidence_lineage_break": "invalidate_dossier",
    "protected_evidence_access": "quarantine_program",
    "authority_escalation": "revoke_actor_and_quarantine",
    "objective_drift": "freeze_program_and_require_amendment",
    "ledger_tamper": "invalidate_ledger_and_escalate",
    "core_boundary_change": "reject_patch",
    "external_evidence_misclassification": "correct_claim_and_requalify",
    "self_approval": "reject_decision_and_escalate",
}


@dataclass(frozen=True)
class Incident:
    incident_id: str
    program_id: str
    category: str
    severity: str
    known_time: str
    evidence_hashes: tuple[str, ...]
    owner: str


def qualify_incident(incident: Incident) -> dict:
    response = INCIDENT_RESPONSES.get(incident.category, "manual_investigation_and_pause")
    return {
        "incident_id": incident.incident_id,
        "program_id": incident.program_id,
        "category": incident.category,
        "severity": incident.severity,
        "required_response": response,
        "known_time": incident.known_time,
        "evidence_hashes": list(incident.evidence_hashes),
        "owner": incident.owner,
    }
