import pytest
from strategy_factory_operations_v3.enums import ControlDecision, EvidenceState
from strategy_factory_operations_v3.golden import NOW, envelope, policy, telemetry
from strategy_factory_operations_v3.health import evaluate_health


def assess(**changes): return evaluate_health(telemetry(**changes), policy(), envelope(), NOW)


def test_clean_health_allows_bounded_risk():
    result = assess()
    assert result.status is EvidenceState.PASS and result.decision is ControlDecision.ALLOW_BOUNDED
    assert result.max_allowed_risk_units == envelope().max_order_risk_units


@pytest.mark.parametrize("changes,reason", [
    ({"last_heartbeat_ms": NOW-policy().heartbeat_timeout_ms-1}, "heartbeat_stale"),
    ({"max_feature_age_ms": policy().max_feature_age_ms+1}, "feature_stale"),
    ({"broker_connected": False}, "broker_disconnected"),
    ({"history_synchronized": False}, "history_unsynchronized"),
    ({"unreserved_action_count": 1}, "unreserved_action"),
    ({"duplicate_action_count": 1}, "duplicate_action"),
    ({"stale_action_count": 1}, "stale_action"),
    ({"critical_error_count": 1}, "critical_error"),
    ({"open_risk_units": envelope().max_open_risk_units+.01}, "open_risk_limit"),
    ({"reserved_risk_units": envelope().max_total_risk_units+.01}, "reserved_risk_limit"),
    ({"daily_pnl_units": -envelope().max_daily_loss_units-.01}, "daily_loss_limit"),
    ({"weekly_pnl_units": -envelope().max_weekly_loss_units-.01}, "weekly_loss_limit"),
    ({"open_positions": envelope().max_positions+1}, "position_count_limit"),
])
def test_hard_health_failures_halt(changes, reason):
    result = assess(**changes)
    assert result.status is EvidenceState.FAIL and result.decision is ControlDecision.SAFE_HALT
    assert result.max_allowed_risk_units == 0 and reason in result.reason_codes


@pytest.mark.parametrize("changes,reason", [
    ({"p99_latency_ms": policy().max_p99_latency_ms+1}, "latency_budget"),
    ({"queue_depth": policy().max_queue_depth+1}, "queue_budget"),
    ({"memory_growth_mb": policy().max_memory_growth_mb+1}, "memory_budget"),
    ({"reject_rate": policy().max_reject_rate+.01}, "broker_reject_budget"),
    ({"drift_score": policy().max_drift_score+.01}, "drift_budget"),
])
def test_soft_budget_breaches_derisk(changes, reason):
    result = assess(**changes)
    assert result.status is EvidenceState.DEGRADED and result.decision is ControlDecision.DERISK
    assert reason in result.reason_codes


def test_future_telemetry_fails():
    result = assess(captured_at_ms=NOW+1, last_heartbeat_ms=NOW)
    assert "telemetry_from_future" in result.reason_codes


def test_risk_headroom_reduces_incremental_authority():
    result = assess(open_risk_units=.24)
    assert result.max_allowed_risk_units == pytest.approx(.01)


def test_no_headroom_returns_zero():
    result = assess(open_risk_units=.25)
    assert result.max_allowed_risk_units == 0
