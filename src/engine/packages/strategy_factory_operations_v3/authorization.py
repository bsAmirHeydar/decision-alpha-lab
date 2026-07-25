from __future__ import annotations

from .canonical import canonical_sha256
from .contracts import (
    CycleAuthorization,
    DeploymentPlan,
    HealthAssessment,
    OperationsIncident,
    OperationsPolicy,
    ReconciliationReport,
    RuntimeLease,
)
from .enums import ControlDecision, DeploymentStage, EvidenceState, IncidentSeverity, IncidentState
from .reconciliation import reconciliation_status


def authorize_cycle(
    plan: DeploymentPlan,
    lease: RuntimeLease,
    health: HealthAssessment,
    reconciliation: ReconciliationReport,
    policy: OperationsPolicy,
    evaluated_at_ms: int,
    incidents: tuple[OperationsIncident, ...] = (),
    manual_kill: bool = False,
) -> CycleAuthorization:
    reasons: list[str] = []
    if manual_kill:
        reasons.append("manual_kill")
    if not (plan.starts_at_ms <= evaluated_at_ms < plan.expires_at_ms):
        reasons.append("plan_inactive")
    if lease.plan_hash != plan.plan_hash:
        reasons.append("lease_plan_mismatch")
    if lease.environment_hash != plan.environment_hash:
        reasons.append("lease_environment_mismatch")
    if lease.generation_hash != plan.generation_hash:
        reasons.append("lease_generation_mismatch")
    if lease.stage is not plan.stage:
        reasons.append("lease_stage_mismatch")
    if not lease.active_at(evaluated_at_ms):
        reasons.append("lease_inactive")
    if health.status is EvidenceState.FAIL:
        reasons.extend(health.reason_codes or ("health_failed",))
    rec_status, rec_reasons = reconciliation_status(reconciliation, plan.environment_hash, plan.generation_hash, evaluated_at_ms, policy.max_reconciliation_age_ms)
    if rec_status is EvidenceState.FAIL:
        reasons.extend(rec_reasons)
    if any(i.state is not IncidentState.CLOSED and i.severity in (IncidentSeverity.HIGH, IncidentSeverity.CRITICAL) for i in incidents):
        reasons.append("high_or_critical_incident_open")
    if reasons:
        decision, authority, risk = ControlDecision.SAFE_HALT, False, 0.0
    elif plan.stage in (DeploymentStage.FROZEN, DeploymentStage.PAPER, DeploymentStage.SHADOW):
        decision, authority, risk = ControlDecision.ALLOW_NO_SEND, False, 0.0
    elif health.status is EvidenceState.DEGRADED:
        decision, authority = ControlDecision.DERISK, False
        risk = 0.0
        reasons.extend(health.reason_codes)
    else:
        decision, authority = ControlDecision.ALLOW_BOUNDED, True
        risk = max(0.0, min(plan.max_risk_units, lease.max_risk_units, health.max_allowed_risk_units))
        if risk == 0:
            decision, authority = ControlDecision.HOLD, False
            reasons.append("zero_incremental_risk")
    health_hash = canonical_sha256(health)
    return CycleAuthorization(
        authorization_id=f"cycle-auth:{plan.plan_id}:{evaluated_at_ms}",
        decision=decision,
        stage=plan.stage,
        evaluated_at_ms=evaluated_at_ms,
        plan_hash=plan.plan_hash,
        lease_hash=lease.lease_hash,
        health_hash=health_hash,
        reconciliation_hash=reconciliation.report_hash,
        authority_order=authority,
        max_incremental_risk_units=risk,
        reason_codes=tuple(sorted(set(reasons))),
    )
