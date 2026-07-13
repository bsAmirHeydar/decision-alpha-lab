from dataclasses import replace
import pytest
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.manual import evaluate_manual
from strategy_factory_policy_v3.contracts import Predicate
from strategy_factory_policy_v3.enums import Action
from strategy_factory_policy_v3.errors import PolicyError

def test_manual_golden_is_eligible():
    d=evaluate_manual(golden_manual(),golden_occurrence()); assert d.eligible and d.action is Action.ENTER_LONG and d.treatment=='market'
def test_manual_wrong_context_ineligible(): assert not evaluate_manual(golden_manual(),replace(golden_occurrence(),context_type='ctx.other')).eligible
def test_manual_threshold_failure_ineligible(): assert not evaluate_manual(golden_manual(),replace(golden_occurrence(),features={**golden_occurrence().features,'score':.2})).eligible
def test_manual_veto_rejects():
    d=evaluate_manual(golden_manual(),replace(golden_occurrence(),features={**golden_occurrence().features,'blocked':True})); assert d.vetoed and d.action is Action.REJECT
def test_manual_exception_changes_risk():
    d=evaluate_manual(golden_manual(),replace(golden_occurrence(),features={**golden_occurrence().features,'liquidity':.1})); assert d.risk_tier=='low' and d.matched_exceptions==('thin_liquidity',)
def test_manual_output_deterministic(): assert evaluate_manual(golden_manual(),golden_occurrence()).decision_hash==evaluate_manual(golden_manual(),golden_occurrence()).decision_hash
def test_manual_unsupported_treatment_fails_closed():
    with pytest.raises(PolicyError): evaluate_manual(golden_manual(),replace(golden_occurrence(),available_treatments=('limit',)))
def test_manual_validity_enforced(): assert not evaluate_manual(replace(golden_manual(),valid_until_ms=1000),golden_occurrence()).eligible
