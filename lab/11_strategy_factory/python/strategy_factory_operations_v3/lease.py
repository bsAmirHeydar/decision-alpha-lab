from __future__ import annotations

from .contracts import DeploymentPlan, DeploymentTarget, OperationsPolicy, RuntimeLease
from .enums import DeploymentStage
from .errors import OperationsError


def issue_runtime_lease(
    plan: DeploymentPlan,
    target: DeploymentTarget,
    policy: OperationsPolicy,
    lease_id: str,
    issued_by: str,
    approved_by: str,
    issued_at_ms: int,
    expires_at_ms: int,
    max_risk_units: float,
) -> RuntimeLease:
    if plan.target_hash != target.target_hash or plan.environment_hash != target.environment_hash:
        raise OperationsError("target_mismatch", "lease target does not match deployment plan")
    if not (plan.starts_at_ms <= issued_at_ms < expires_at_ms <= plan.expires_at_ms):
        raise OperationsError("lease_window", "lease must remain within deployment plan window")
    if expires_at_ms - issued_at_ms > policy.max_lease_minutes * 60_000:
        raise OperationsError("lease_duration", "lease exceeds maximum duration")
    if policy.require_distinct_operator_approver and issued_by == approved_by:
        raise OperationsError("lease_sod", "lease issuer and approver must be distinct")
    live = plan.stage in (DeploymentStage.MICRO_LIVE, DeploymentStage.LIMITED_LIVE, DeploymentStage.PRODUCTION)
    effective_risk = max_risk_units if live else 0.0
    if effective_risk < 0 or effective_risk > plan.max_risk_units:
        raise OperationsError("lease_risk", "lease exceeds deployment plan risk")
    return RuntimeLease(
        lease_id=lease_id,
        schema_version="1.0.0",
        plan_hash=plan.plan_hash,
        environment_hash=plan.environment_hash,
        generation_hash=plan.generation_hash,
        stage=plan.stage,
        account_hashes=target.account_hashes,
        allowed_symbols=target.allowed_symbols,
        max_risk_units=effective_risk,
        issued_by=issued_by,
        approved_by=approved_by,
        issued_at_ms=issued_at_ms,
        expires_at_ms=expires_at_ms,
    )


def revoke_runtime_lease(lease: RuntimeLease, revoked_at_ms: int, reason: str) -> RuntimeLease:
    if not reason.strip():
        raise OperationsError("revocation_reason", "lease revocation requires a reason")
    if not lease.issued_at_ms <= revoked_at_ms <= lease.expires_at_ms:
        raise OperationsError("revocation_time", "revocation time is outside lease window")
    return RuntimeLease(
        lease_id=lease.lease_id,
        schema_version=lease.schema_version,
        plan_hash=lease.plan_hash,
        environment_hash=lease.environment_hash,
        generation_hash=lease.generation_hash,
        stage=lease.stage,
        account_hashes=lease.account_hashes,
        allowed_symbols=lease.allowed_symbols,
        max_risk_units=lease.max_risk_units,
        issued_by=lease.issued_by,
        approved_by=lease.approved_by,
        issued_at_ms=lease.issued_at_ms,
        expires_at_ms=lease.expires_at_ms,
        revoked_at_ms=revoked_at_ms,
        revocation_reason=reason,
    )
