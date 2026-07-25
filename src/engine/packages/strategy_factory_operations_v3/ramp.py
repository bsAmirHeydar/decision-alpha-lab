from __future__ import annotations

from .contracts import OperationsPolicy, ProspectiveWindow, RampDecision, RiskEnvelope
from .enums import DeploymentStage, RampVerdict

_NEXT = {
    DeploymentStage.PAPER: DeploymentStage.SHADOW,
    DeploymentStage.SHADOW: DeploymentStage.MICRO_LIVE,
    DeploymentStage.MICRO_LIVE: DeploymentStage.LIMITED_LIVE,
    DeploymentStage.LIMITED_LIVE: DeploymentStage.PRODUCTION,
}


def evaluate_ramp(
    window: ProspectiveWindow,
    requested_stage: DeploymentStage,
    policy: OperationsPolicy,
    next_envelope: RiskEnvelope,
    evaluated_at_ms: int,
) -> RampDecision:
    reasons: list[str] = []
    if _NEXT.get(window.stage) is not requested_stage:
        reasons.append("non_adjacent_stage_request")
    if window.ended_at_ms > evaluated_at_ms:
        reasons.append("window_from_future")
    key = requested_stage.value
    if window.sessions < policy.minimum_stage_sessions.get(key, 10**12):
        reasons.append("insufficient_sessions")
    if window.events < policy.minimum_stage_events.get(key, 10**12):
        reasons.append("insufficient_events")
    if window.calendar_days < policy.minimum_stage_days.get(key, 10**12):
        reasons.append("insufficient_calendar_days")
    if window.reconciliations <= 0 or window.reconciliation_failures:
        reasons.append("reconciliation_not_clean")
    if window.high_incidents or window.critical_incidents:
        reasons.append("material_incident_present")
    if window.policy_breaches:
        reasons.append("policy_breach_present")
    if window.reject_rate > policy.max_reject_rate:
        reasons.append("reject_rate_exceeded")
    if window.p99_latency_ms > policy.max_p99_latency_ms:
        reasons.append("latency_exceeded")
    if window.drift_score > policy.max_drift_score:
        reasons.append("drift_exceeded")
    if window.max_drawdown_units > next_envelope.max_daily_loss_units:
        reasons.append("drawdown_exceeded")
    if reasons:
        verdict, risk = RampVerdict.BLOCKED, 0.0
    else:
        verdict, risk = RampVerdict.ELIGIBLE_FOR_HUMAN_APPROVAL, next_envelope.max_total_risk_units
    return RampDecision(
        decision_id=f"ramp:{window.window_id}:{requested_stage.value}:{evaluated_at_ms}",
        current_stage=window.stage,
        requested_stage=requested_stage,
        verdict=verdict,
        evaluated_at_ms=evaluated_at_ms,
        window_hash=window.window_hash,
        reason_codes=tuple(sorted(set(reasons))),
        maximum_risk_units=risk,
        requires_human_approval=True,
    )
