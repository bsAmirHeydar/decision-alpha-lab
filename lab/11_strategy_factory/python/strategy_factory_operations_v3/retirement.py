from __future__ import annotations

from .contracts import DeploymentPlan, RetirementManifest
from .errors import OperationsError


def compile_retirement_manifest(
    plan: DeploymentPlan,
    release_manifest_hash: str,
    retired_at_ms: int,
    retired_by: str,
    approved_by: str,
    positions_flat: bool,
    reservations_zero: bool,
    leases_revoked: bool,
    evidence_archive_hash: str,
    retention_until_ms: int,
    reason: str,
    open_high_or_critical_incidents: int = 0,
) -> RetirementManifest:
    if open_high_or_critical_incidents:
        raise OperationsError("retirement_incident", "material incidents must be resolved or transferred before retirement")
    return RetirementManifest(
        retirement_id=f"retirement:{plan.plan_id}:{retired_at_ms}",
        release_manifest_hash=release_manifest_hash,
        plan_hash=plan.plan_hash,
        environment_hash=plan.environment_hash,
        generation_hash=plan.generation_hash,
        retired_at_ms=retired_at_ms,
        retired_by=retired_by,
        approved_by=approved_by,
        positions_flat=positions_flat,
        reservations_zero=reservations_zero,
        leases_revoked=leases_revoked,
        evidence_archive_hash=evidence_archive_hash,
        retention_until_ms=retention_until_ms,
        reason=reason,
    )
