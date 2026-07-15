from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.enums import EvidenceStatus, GateName, ReleaseStage
from strategy_factory_qualification_v3.golden import NOW, policy, stage_evidence
from strategy_factory_qualification_v3.staging import evaluate_stage


def test_paper_stage_passes():
    result = evaluate_stage(stage_evidence(ReleaseStage.PAPER), policy(), NOW)
    assert result.status is EvidenceStatus.PASS and result.gate is GateName.PAPER


def test_micro_live_requires_explicit_approval():
    evidence = replace(stage_evidence(ReleaseStage.MICRO_LIVE), human_approval_id="")
    assert "micro_live_human_approval_missing" in evaluate_stage(evidence, policy(), NOW).reason_codes


@pytest.mark.parametrize("field,value,reason", [
    ("sessions", 0, "prospective_sessions_below_minimum"),
    ("decision_events", 0, "prospective_events_below_minimum"),
    ("reconciliation_mismatches", 1, "prospective_reconciliation_mismatch"),
    ("duplicate_actions", 1, "prospective_duplicate_action"),
    ("critical_incidents", 1, "prospective_critical_incident"),
])
def test_stage_failures_are_non_compensatory(field, value, reason):
    evidence = replace(stage_evidence(ReleaseStage.PAPER), **{field: value})
    assert reason in evaluate_stage(evidence, policy(), NOW).reason_codes


def test_broker_reject_rate_is_enforced():
    evidence = replace(stage_evidence(ReleaseStage.PAPER), broker_rejections=10, order_intents=10)
    assert "broker_reject_rate" in evaluate_stage(evidence, policy(), NOW).reason_codes


def test_micro_live_risk_cap_is_enforced():
    evidence = replace(stage_evidence(ReleaseStage.MICRO_LIVE), max_realized_risk_units=0.3, max_allowed_risk_units=0.5)
    assert "micro_live_risk_budget" in evaluate_stage(evidence, policy(), NOW).reason_codes


def test_invalid_stage_is_rejected():
    with pytest.raises(ValueError):
        evaluate_stage(replace(stage_evidence(ReleaseStage.PAPER), stage=ReleaseStage.FROZEN), policy(), NOW)
