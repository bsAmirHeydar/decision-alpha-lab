import dataclasses,pytest
from strategy_factory_runtime_v3.golden import *
from strategy_factory_runtime_v3.host import BoundedRuntimeHost
from strategy_factory_runtime_v3.journal import DecisionJournal
from strategy_factory_runtime_v3.enums import *
from strategy_factory_runtime_v3.errors import *

def host(**kw):
    m,p,model,e,data=golden_bundle();return BoundedRuntimeHost(m,p,model,e,signature_secret=b'uce-i14-test-secret',**kw)
def test_shadow_decision_has_no_order_authority():
    d=host().decide(golden_request());assert d.disposition is RuntimeDisposition.DECIDED;assert d.label=='enter_long';assert not d.order_authority
def test_same_request_is_idempotent():
    h=host();r=golden_request();assert h.decide(r)==h.decide(r);assert len(h.journal.snapshot())==1
def test_occurrence_duplicate_with_different_decision_rejected():
    j=DecisionJournal();d=host(journal=j).decide(golden_request());from strategy_factory_runtime_v3.contracts import RuntimeDecision
    conflict=dataclasses.replace(d,decision_id='other',request_id='other',label='no_action')
    with pytest.raises(DuplicateDecisionError):j.append(conflict)
def test_kill_switch_is_non_compensatory():
    r=dataclasses.replace(golden_request(),kill_switch=True);d=host().decide(r);assert d.disposition is RuntimeDisposition.REJECTED;assert d.label=='reject';assert 'kill_switch' in d.reasons
def test_stale_context_rejected():
    r=dataclasses.replace(golden_request(),known_time_ms=1,received_at_ms=100000)
    with pytest.raises(RuntimeContractError):host(max_context_age_ms=10).decide(r)
def test_live_mode_not_in_bundle_support():
    r=dataclasses.replace(golden_request(),mode=RuntimeMode.LIVE)
    with pytest.raises(ActivationError):host().decide(r)
def test_wrong_signature_refuses_host_activation():
    m,p,model,e,data=golden_bundle()
    with pytest.raises(BundleValidationError):BoundedRuntimeHost(m,p,model,e,signature_secret=b'wrong')
def test_custom_policy_executor_is_bounded():
    def executor(req,label,scores):return RuntimeDisposition.ABSTAINED,'no_action',('low_confidence',)
    d=host(policy_executor=executor).decide(golden_request());assert d.disposition is RuntimeDisposition.ABSTAINED;assert d.label=='no_action'
def test_restart_restores_journal_without_duplicate():
    h1=host();d1=h1.decide(golden_request());j=DecisionJournal();j.restore(h1.journal.snapshot());h2=host(journal=j);d2=h2.decide(golden_request());assert d1.decision_hash==d2.decision_hash;assert len(j.snapshot())==1
def test_unknown_feature_fails_before_inference():
    r=dataclasses.replace(golden_request(),features={**golden_request().features,'future':1})
    with pytest.raises(RuntimeContractError):host().decide(r)
