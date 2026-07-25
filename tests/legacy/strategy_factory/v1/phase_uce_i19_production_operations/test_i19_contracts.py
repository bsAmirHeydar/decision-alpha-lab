from dataclasses import replace
import pytest

from strategy_factory_operations_v3.contracts import (
    ChangeRequest, DeploymentTarget, OperationsIncident, RetirementManifest,
    RiskEnvelope, RuntimeLease, TelemetrySnapshot,
)
from strategy_factory_operations_v3.enums import DeploymentStage, IncidentSeverity, IncidentState
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.golden import H1, H2, H3, H4, H5, H6, NOW, envelope, target, telemetry


def test_target_hash_is_deterministic():
    assert target().target_hash == target().target_hash


@pytest.mark.parametrize("field", ["environment_hash", "broker_server_hash"])
def test_target_rejects_invalid_hash(field):
    values = target().__dict__.copy(); values[field] = "bad"
    with pytest.raises(ValueError): DeploymentTarget(**values)


def test_target_rejects_duplicate_accounts():
    with pytest.raises(OperationsError):
        DeploymentTarget("x", H1, H2, (H3, H3), ("EURUSD",), ("t",), "UTC", NOW)


def test_target_rejects_duplicate_symbols():
    with pytest.raises(OperationsError):
        DeploymentTarget("x", H1, H2, (H3,), ("EURUSD", "EURUSD"), ("t",), "UTC", NOW)


def test_target_rejects_duplicate_terminals():
    with pytest.raises(OperationsError):
        DeploymentTarget("x", H1, H2, (H3,), ("EURUSD",), ("t", "t"), "UTC", NOW)


@pytest.mark.parametrize("field,value", [
    ("max_total_risk_units", -1), ("max_open_risk_units", -1),
    ("max_order_risk_units", -1), ("max_daily_loss_units", -1),
    ("max_weekly_loss_units", -1), ("max_positions", -1),
    ("max_orders_per_minute", -1),
])
def test_risk_envelope_rejects_negative_fields(field, value):
    values = envelope().__dict__.copy(); values[field] = value
    with pytest.raises(OperationsError): RiskEnvelope(**values)


def test_risk_envelope_rejects_open_above_total():
    values = envelope().__dict__.copy(); values["max_open_risk_units"] = 0.3
    with pytest.raises(OperationsError): RiskEnvelope(**values)


def test_risk_envelope_rejects_order_above_open():
    values = envelope().__dict__.copy(); values["max_order_risk_units"] = 0.3
    with pytest.raises(OperationsError): RiskEnvelope(**values)


@pytest.mark.parametrize("field,value", [
    ("max_feature_age_ms", -1), ("queue_depth", -1), ("open_positions", -1),
    ("duplicate_action_count", -1), ("stale_action_count", -1),
    ("unreserved_action_count", -1), ("critical_error_count", -1),
    ("p99_latency_ms", -1), ("memory_growth_mb", -1),
    ("open_risk_units", -1), ("reserved_risk_units", -1),
    ("reject_rate", -0.1), ("drift_score", -1),
])
def test_telemetry_rejects_negative_metrics(field, value):
    values = telemetry().__dict__.copy(); values[field] = value
    with pytest.raises(OperationsError): TelemetrySnapshot(**values)


def test_telemetry_rejects_heartbeat_from_future():
    values = telemetry().__dict__.copy(); values["last_heartbeat_ms"] = NOW + 1
    with pytest.raises(OperationsError): TelemetrySnapshot(**values)


def test_runtime_lease_active_semantics():
    lease = RuntimeLease("l", "1.0.0", H1, H2, H3, DeploymentStage.MICRO_LIVE, (H4,), ("EURUSD",), 0.1, "a", "b", 10, 20)
    assert not lease.active_at(9)
    assert lease.active_at(10)
    assert lease.active_at(19)
    assert not lease.active_at(20)


def test_revoked_lease_is_inactive():
    lease = RuntimeLease("l", "1.0.0", H1, H2, H3, DeploymentStage.MICRO_LIVE, (H4,), ("EURUSD",), 0.1, "a", "b", 10, 20, 15, "kill")
    assert not lease.active_at(14)


def test_change_request_rejects_noop():
    with pytest.raises(OperationsError): ChangeRequest("c", "u", NOW, H1, {"x": ("1", "1")}, False, (H2,))


def test_closed_incident_requires_closer():
    with pytest.raises(OperationsError):
        OperationsIncident("i", IncidentSeverity.HIGH, IncidentState.CLOSED, NOW, NOW+1, NOW+2, NOW+3, H1, H2, "x", (H3,), "owner")


def test_retirement_requires_sod():
    with pytest.raises(OperationsError):
        RetirementManifest("r", H1, H2, H3, H4, NOW, "same", "same", True, True, True, H5, NOW+1, "done")
