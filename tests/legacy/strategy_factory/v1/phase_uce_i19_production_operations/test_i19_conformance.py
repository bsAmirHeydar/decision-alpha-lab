from dataclasses import replace
import pytest
from strategy_factory_operations_v3.conformance import assert_authorization_is_bounded
from strategy_factory_operations_v3.enums import ControlDecision, DeploymentStage
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.golden import H1, NOW, envelope, policy, reconciliation, telemetry
from strategy_factory_operations_v3.orchestrator import evaluate_operating_cycle


def test_clean_authorization_conforms(live_plan, live_lease):
    auth=evaluate_operating_cycle(live_plan,live_lease,telemetry(),reconciliation(),policy(),envelope(),NOW)
    assert_authorization_is_bounded(auth, live_plan, live_lease)


def test_lineage_mismatch_is_detected(live_plan, live_lease):
    auth=evaluate_operating_cycle(live_plan,live_lease,telemetry(),reconciliation(),policy(),envelope(),NOW)
    with pytest.raises(OperationsError, match="authorization_lineage"): assert_authorization_is_bounded(replace(auth, plan_hash=H1), live_plan, live_lease)


def test_risk_escalation_is_detected(live_plan, live_lease):
    auth=evaluate_operating_cycle(live_plan,live_lease,telemetry(),reconciliation(),policy(),envelope(),NOW)
    with pytest.raises(OperationsError, match="authorization_risk"): assert_authorization_is_bounded(replace(auth, max_incremental_risk_units=.3), live_plan, live_lease)


def test_invalid_decision_authority_is_detected(live_plan, live_lease):
    auth=evaluate_operating_cycle(live_plan,live_lease,telemetry(),reconciliation(),policy(),envelope(),NOW)
    with pytest.raises(OperationsError, match="decision_authority"): assert_authorization_is_bounded(replace(auth, decision=ControlDecision.HOLD), live_plan, live_lease)
