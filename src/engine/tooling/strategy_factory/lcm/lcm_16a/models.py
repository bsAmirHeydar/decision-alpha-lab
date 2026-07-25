from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditVerificationResult:
    audit_id: str
    baseline_count: int
    amendment_count: int
    unchanged_count: int
    missing_count: int
    deterministic_gate_status: str
    external_evidence_status: str
    closure_decision: str
    validation_status: str
