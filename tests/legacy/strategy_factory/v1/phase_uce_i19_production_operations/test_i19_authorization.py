from dataclasses import replace
import pytest

from strategy_factory_operations_v3.authorization import authorize_cycle
from strategy_factory_operations_v3.enums import ControlDecision, DeploymentStage, IncidentSeverity
from strategy_factory_operations_v3.golden import H4, NOW, envelope, policy, reconciliation, telemetry
from strategy_factory_operations_v3.health import evaluate_health
from strategy_factory_operations_v3.incidents import open_incident
from strategy_factory_operations_v3.orchestrator import evaluate_operating_cycle


def auth(plan, lease, **kwargs):
    health = evaluate_health(telemetry(), policy(), envelope(), NOW)
    args = dict(plan=plan, lease=lease, health=health, reconciliation=reconciliation(), policy=policy(), evaluated_at_ms=NOW)
    args.update(kwargs)
    return authorize_cycle(**args)


def test_clean_live_cycle_is_bounded(live_plan, live_lease):
    result = auth(live_plan, live_lease)
    assert result.decision is ControlDecision.ALLOW_BOUNDED and result.authority_order
    assert result.max_incremental_risk_units == .05


def test_manual_kill_halts(live_plan, live_lease):
    result = auth(live_plan, live_lease, manual_kill=True)
    assert result.decision is ControlDecision.SAFE_HALT and "manual_kill" in result.reason_codes


@pytest.mark.parametrize("lease_change,reason", [
    ({"plan_hash": H4}, "lease_plan_mismatch"),
    ({"environment_hash": H4}, "lease_environment_mismatch"),
    ({"generation_hash": H4}, "lease_generation_mismatch"),
    ({"stage": DeploymentStage.LIMITED_LIVE}, "lease_stage_mismatch"),
    ({"expires_at_ms": NOW}, "lease_inactive"),
])
def test_lease_lineage_failures_halt(live_plan, live_lease, lease_change, reason):
    result = auth(live_plan, replace(live_lease, **lease_change))
    assert result.decision is ControlDecision.SAFE_HALT and reason in result.reason_codes


def test_expired_plan_halts(live_plan, live_lease):
    plan = replace(live_plan, expires_at_ms=NOW)
    lease = replace(live_lease, plan_hash=plan.plan_hash, expires_at_ms=NOW)
    result = auth(plan, lease)
    assert "plan_inactive" in result.reason_codes


def test_failed_health_halts(live_plan, live_lease):
    health = evaluate_health(telemetry(broker_connected=False), policy(), envelope(), NOW)
    result = auth(live_plan, live_lease, health=health)
    assert result.decision is ControlDecision.SAFE_HALT and "broker_disconnected" in result.reason_codes


def test_degraded_health_derisks_without_order_authority(live_plan, live_lease):
    health = evaluate_health(telemetry(p99_latency_ms=101), policy(), envelope(), NOW)
    result = auth(live_plan, live_lease, health=health)
    assert result.decision is ControlDecision.DERISK and not result.authority_order


def test_reconciliation_failure_halts(live_plan, live_lease):
    result = auth(live_plan, live_lease, reconciliation=reconciliation(orphan_order_count=1))
    assert result.decision is ControlDecision.SAFE_HALT and "orphan_order_count" in result.reason_codes


@pytest.mark.parametrize("severity", [IncidentSeverity.HIGH, IncidentSeverity.CRITICAL])
def test_material_open_incident_halts(live_plan, live_lease, severity):
    incident = open_incident("i", severity, NOW-1, live_plan.environment_hash, live_plan.generation_hash, "x", (H4,), "owner")
    result = auth(live_plan, live_lease, incidents=(incident,))
    assert "high_or_critical_incident_open" in result.reason_codes


def test_warning_incident_does_not_halt(live_plan, live_lease):
    incident = open_incident("i", IncidentSeverity.WARNING, NOW-1, live_plan.environment_hash, live_plan.generation_hash, "x", (H4,), "owner")
    assert auth(live_plan, live_lease, incidents=(incident,)).decision is ControlDecision.ALLOW_BOUNDED


def test_orchestrator_matches_direct_path(live_plan, live_lease):
    result = evaluate_operating_cycle(live_plan, live_lease, telemetry(), reconciliation(), policy(), envelope(), NOW)
    assert result.decision is ControlDecision.ALLOW_BOUNDED


def test_zero_headroom_holds(live_plan, live_lease):
    result = evaluate_operating_cycle(live_plan, live_lease, telemetry(open_risk_units=.25), reconciliation(), policy(), envelope(), NOW)
    assert result.decision is ControlDecision.HOLD and not result.authority_order
