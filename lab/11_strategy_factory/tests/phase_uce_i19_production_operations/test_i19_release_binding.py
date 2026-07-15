from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.enums import ReleaseStage
from strategy_factory_operations_v3.enums import DeploymentStage
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.golden import NOW, envelope, policy, release, target
from strategy_factory_operations_v3.release_binding import compile_deployment_plan


def build(stage=DeploymentStage.MICRO_LIVE, risk=0.25, rel=None, tgt=None, op="op", app="app", approved=NOW-1000, starts=NOW-500, expires=NOW+1000):
    return compile_deployment_plan(rel or release(), tgt or target(), envelope(), policy(), stage, risk, op, app, approved, starts, expires)


def test_live_plan_binds_exact_i18_release():
    plan = build()
    assert plan.authority_order and plan.authority_broker
    assert plan.release_manifest_hash == release().manifest_hash
    assert plan.environment_hash == target().environment_hash


@pytest.mark.parametrize("stage", [DeploymentStage.FROZEN, DeploymentStage.PAPER, DeploymentStage.SHADOW])
def test_non_live_stages_have_zero_authority(stage):
    rel_stage = {DeploymentStage.FROZEN: ReleaseStage.FROZEN, DeploymentStage.PAPER: ReleaseStage.PAPER, DeploymentStage.SHADOW: ReleaseStage.SHADOW}[stage]
    plan = build(stage=stage, risk=99, rel=release(rel_stage, 0))
    assert plan.max_risk_units == 0 and not plan.authority_order and not plan.authority_broker


@pytest.mark.parametrize("requested", [DeploymentStage.LIMITED_LIVE, DeploymentStage.PRODUCTION])
def test_stage_escalation_is_rejected(requested):
    with pytest.raises(OperationsError, match="stage_escalation"): build(stage=requested)


def test_environment_mismatch_is_rejected():
    tgt = replace(target(), environment_hash="9"*64)
    with pytest.raises(OperationsError, match="environment_mismatch"): build(tgt=tgt)


def test_plan_cannot_outlive_release():
    with pytest.raises(OperationsError, match="release_expired"): build(expires=release().expires_at_ms + 1)


def test_expired_release_is_rejected():
    rel = replace(release(), expires_at_ms=NOW-1)
    with pytest.raises(OperationsError, match="release_expired"): build(rel=rel)


def test_operator_and_approver_must_be_distinct():
    with pytest.raises(OperationsError, match="separation_of_duties"): build(op="same", app="same")


@pytest.mark.parametrize("risk", [-0.1, 0.26, 100])
def test_risk_escalation_is_rejected(risk):
    with pytest.raises(OperationsError, match="risk_escalation"): build(risk=risk)


def test_live_release_requires_broker_and_order_authority():
    rel = replace(release(), authority_order=False)
    with pytest.raises(OperationsError, match="release_authority"): build(rel=rel)


@pytest.mark.parametrize("field,value", [
    ("account_hashes", ()), ("allowed_symbols", ()), ("terminal_instance_ids", ()),
])
def test_live_target_requires_exact_bindings(field, value):
    tgt = replace(target(), **{field:value})
    with pytest.raises(OperationsError, match="target_binding"): build(tgt=tgt)


def test_plan_identity_is_deterministic():
    assert build().plan_hash == build().plan_hash


def test_plan_timeline_rejects_start_before_approval():
    with pytest.raises(OperationsError, match="plan_timeline"): build(approved=NOW, starts=NOW-1)
