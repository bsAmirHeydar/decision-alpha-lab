import pytest
from strategy_factory_operations_v3.change_control import classify_change
from strategy_factory_operations_v3.contracts import ChangeRequest
from strategy_factory_operations_v3.enums import ChangeClass
from strategy_factory_operations_v3.golden import H1, H2, NOW, policy


def req(changes, emergency=False): return ChangeRequest("c", "user", NOW, H1, changes, emergency, (H2,))


@pytest.mark.parametrize("field", ["documentation", "runbook", "contact_roster", "dashboard_label"])
def test_documentation_changes_are_approved(field):
    result = classify_change(req({field:("a","b")}), policy(), NOW)
    assert result.classification is ChangeClass.DOCUMENTATION_ONLY and result.approved and not result.requalification_required


@pytest.mark.parametrize("field", ["alert_route", "log_retention_days", "dashboard_layout", "ticket_queue"])
def test_non_authority_changes_are_approved(field):
    result = classify_change(req({field:("a","b")}), policy(), NOW)
    assert result.classification is ChangeClass.NON_AUTHORITY_OPERATIONS and result.approved


@pytest.mark.parametrize("field", [
    "source_commit", "qualification_report_hash", "release_manifest_hash", "environment_hash",
    "generation_hash", "rollback_generation_hash", "broker_server_hash", "account_hashes",
    "symbol_spec_hash", "context_spec_hash", "feature_manifest_hash", "model_hash",
    "calibrator_hash", "policy_graph_hash", "treatment_hash", "economics_policy_hash", "risk_envelope_hash",
])
def test_authority_changes_require_requalification(field):
    result = classify_change(req({field:("a","b")}), policy(), NOW)
    assert result.classification is ChangeClass.QUALIFICATION_INVALIDATING
    assert not result.approved and result.requalification_required


@pytest.mark.parametrize("field", ["active_generation_bytes", "live_feature_order", "open_position_identity", "reservation_ledger"])
def test_forbidden_hot_changes_are_denied(field):
    result = classify_change(req({field:("a","b")}), policy(), NOW)
    assert result.classification is ChangeClass.FORBIDDEN_HOT_CHANGE and not result.approved


@pytest.mark.parametrize("field,old,new", [
    ("max_risk_units", "1", ".5"), ("max_positions", "4", "2"),
    ("max_orders_per_minute", "10", "5"), ("allowed_symbols", "EURUSD,GBPUSD", "EURUSD"),
])
def test_emergency_risk_reduction_is_approved(field, old, new):
    result = classify_change(req({field:(old,new)}, True), policy(), NOW)
    assert result.classification is ChangeClass.RISK_REDUCTION and result.approved and not result.requalification_required


@pytest.mark.parametrize("field,old,new", [
    ("max_risk_units", ".5", "1"), ("max_positions", "2", "4"),
    ("allowed_symbols", "EURUSD", "EURUSD,GBPUSD"),
])
def test_emergency_risk_increase_is_denied(field, old, new):
    result = classify_change(req({field:(old,new)}, True), policy(), NOW)
    assert result.classification is ChangeClass.FORBIDDEN_HOT_CHANGE and not result.approved


def test_unknown_change_is_fail_closed():
    result = classify_change(req({"mystery":("a","b")}), policy(), NOW)
    assert result.requalification_required and not result.approved
