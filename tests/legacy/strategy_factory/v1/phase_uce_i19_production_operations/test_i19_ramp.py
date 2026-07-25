import pytest
from strategy_factory_operations_v3.enums import DeploymentStage, RampVerdict
from strategy_factory_operations_v3.golden import NOW, envelope, policy, window
from strategy_factory_operations_v3.ramp import evaluate_ramp


def decide(stage=DeploymentStage.SHADOW, requested=DeploymentStage.MICRO_LIVE, **changes):
    return evaluate_ramp(window(stage, **changes), requested, policy(), envelope(), NOW)


def test_clean_adjacent_ramp_is_only_eligible_for_human_approval():
    result = decide()
    assert result.verdict is RampVerdict.ELIGIBLE_FOR_HUMAN_APPROVAL
    assert result.requires_human_approval and result.maximum_risk_units == envelope().max_total_risk_units


@pytest.mark.parametrize("stage,requested", [
    (DeploymentStage.PAPER, DeploymentStage.MICRO_LIVE),
    (DeploymentStage.SHADOW, DeploymentStage.LIMITED_LIVE),
    (DeploymentStage.MICRO_LIVE, DeploymentStage.PRODUCTION),
    (DeploymentStage.PRODUCTION, DeploymentStage.PRODUCTION),
])
def test_non_adjacent_ramp_is_blocked(stage, requested):
    result = decide(stage, requested)
    assert result.verdict is RampVerdict.BLOCKED and "non_adjacent_stage_request" in result.reason_codes


@pytest.mark.parametrize("changes,reason", [
    ({"ended_at_ms": NOW+1}, "window_from_future"),
    ({"sessions": 0}, "insufficient_sessions"),
    ({"events": 0}, "insufficient_events"),
    ({"calendar_days": 0}, "insufficient_calendar_days"),
    ({"reconciliations": 0}, "reconciliation_not_clean"),
    ({"reconciliation_failures": 1}, "reconciliation_not_clean"),
    ({"high_incidents": 1}, "material_incident_present"),
    ({"critical_incidents": 1}, "material_incident_present"),
    ({"policy_breaches": 1}, "policy_breach_present"),
    ({"reject_rate": .06}, "reject_rate_exceeded"),
    ({"p99_latency_ms": 101}, "latency_exceeded"),
    ({"drift_score": .21}, "drift_exceeded"),
    ({"max_drawdown_units": .16}, "drawdown_exceeded"),
])
def test_ramp_blockers(changes, reason):
    result = decide(**changes)
    assert result.verdict is RampVerdict.BLOCKED and reason in result.reason_codes


def test_each_adjacent_stage_can_be_evaluated():
    pairs = [(DeploymentStage.PAPER, DeploymentStage.SHADOW), (DeploymentStage.SHADOW, DeploymentStage.MICRO_LIVE), (DeploymentStage.MICRO_LIVE, DeploymentStage.LIMITED_LIVE), (DeploymentStage.LIMITED_LIVE, DeploymentStage.PRODUCTION)]
    for current, requested in pairs:
        result = decide(current, requested)
        assert "non_adjacent_stage_request" not in result.reason_codes
