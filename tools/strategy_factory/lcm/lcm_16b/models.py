from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProgramClosureVerificationResult:
    closure_id: str
    phase_count: int
    control_plane_path_count: int
    local_recovery_status: str
    external_evidence_status: str
    approval_status: str
    program_closure_decision: str
    certificate_status: str
    validation_status: str
