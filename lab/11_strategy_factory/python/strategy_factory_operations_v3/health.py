from __future__ import annotations

from .contracts import HealthAssessment, OperationsPolicy, RiskEnvelope, TelemetrySnapshot
from .enums import ControlDecision, EvidenceState


def evaluate_health(
    telemetry: TelemetrySnapshot,
    policy: OperationsPolicy,
    envelope: RiskEnvelope,
    evaluated_at_ms: int,
) -> HealthAssessment:
    fail: list[str] = []
    degraded: list[str] = []
    if telemetry.captured_at_ms > evaluated_at_ms:
        fail.append("telemetry_from_future")
    if evaluated_at_ms - telemetry.last_heartbeat_ms > policy.heartbeat_timeout_ms:
        fail.append("heartbeat_stale")
    if telemetry.max_feature_age_ms > policy.max_feature_age_ms:
        fail.append("feature_stale")
    if not telemetry.broker_connected:
        fail.append("broker_disconnected")
    if not telemetry.history_synchronized:
        fail.append("history_unsynchronized")
    if telemetry.unreserved_action_count:
        fail.append("unreserved_action")
    if telemetry.duplicate_action_count:
        fail.append("duplicate_action")
    if telemetry.stale_action_count:
        fail.append("stale_action")
    if telemetry.critical_error_count:
        fail.append("critical_error")
    if telemetry.open_risk_units > envelope.max_open_risk_units:
        fail.append("open_risk_limit")
    if telemetry.reserved_risk_units > envelope.max_total_risk_units:
        fail.append("reserved_risk_limit")
    if -telemetry.daily_pnl_units > envelope.max_daily_loss_units:
        fail.append("daily_loss_limit")
    if -telemetry.weekly_pnl_units > envelope.max_weekly_loss_units:
        fail.append("weekly_loss_limit")
    if telemetry.open_positions > envelope.max_positions:
        fail.append("position_count_limit")
    if telemetry.p99_latency_ms > policy.max_p99_latency_ms:
        degraded.append("latency_budget")
    if telemetry.queue_depth > policy.max_queue_depth:
        degraded.append("queue_budget")
    if telemetry.memory_growth_mb > policy.max_memory_growth_mb:
        degraded.append("memory_budget")
    if telemetry.reject_rate > policy.max_reject_rate:
        degraded.append("broker_reject_budget")
    if telemetry.drift_score > policy.max_drift_score:
        degraded.append("drift_budget")
    if fail:
        status, decision, risk = EvidenceState.FAIL, ControlDecision.SAFE_HALT, 0.0
        reasons = tuple(sorted(set(fail + degraded)))
    elif degraded:
        status, decision = EvidenceState.DEGRADED, ControlDecision.DERISK
        risk = max(0.0, min(envelope.max_order_risk_units, envelope.max_open_risk_units - telemetry.open_risk_units))
        reasons = tuple(sorted(set(degraded)))
    else:
        status, decision = EvidenceState.PASS, ControlDecision.ALLOW_BOUNDED
        risk = max(0.0, min(envelope.max_order_risk_units, envelope.max_open_risk_units - telemetry.open_risk_units, envelope.max_total_risk_units - telemetry.reserved_risk_units))
        reasons = ()
    return HealthAssessment(
        assessment_id=f"health:{telemetry.snapshot_id}:{evaluated_at_ms}",
        status=status,
        decision=decision,
        evaluated_at_ms=evaluated_at_ms,
        reason_codes=reasons,
        telemetry_hash=telemetry.snapshot_hash,
        max_allowed_risk_units=risk,
    )
