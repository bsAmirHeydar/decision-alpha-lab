import dataclasses,pytest
from strategy_factory_runtime_v3.golden import *
from strategy_factory_runtime_v3.failure import qualify_failures
from strategy_factory_runtime_v3.replay import replay,assert_prefix_stable
from strategy_factory_runtime_v3.host import BoundedRuntimeHost
from strategy_factory_runtime_v3.enums import *

def make_host():
    m,p,model,e,data=golden_bundle();return BoundedRuntimeHost(m,p,model,e,signature_secret=b'uce-i14-test-secret')
def test_clean_failure_report_passes():
    m,*_=golden_bundle();r=qualify_failures(m.bundle_hash);assert r.passed;assert not any(f.detected and f.severity=='critical' for f in r.findings)
@pytest.mark.parametrize('field,code',[('artifact_hash_ok',FailureCode.CORRUPT_ARTIFACT),('feature_order_ok',FailureCode.FEATURE_ORDER_MISMATCH),('restart_reconciled',FailureCode.RESTART_RECONCILIATION),('signature_ok',FailureCode.SIGNATURE_FAILURE),('parity_ok',FailureCode.PARITY_FAILURE),('kill_switch_safe',FailureCode.KILL_SWITCH)])
def test_critical_failure_vetoes_report(field,code):
    m,*_=golden_bundle();r=qualify_failures(m.bundle_hash,**{field:False});assert not r.passed;assert any(f.code is code and f.detected for f in r.findings)
@pytest.mark.parametrize('field,code',[('context_fresh',FailureCode.STALE_CONTEXT),('symbol_available',FailureCode.SYMBOL_UNAVAILABLE),('inference_ok',FailureCode.INFERENCE_FAILURE),('latency_ok',FailureCode.LATENCY_BREACH),('queue_ok',FailureCode.QUEUE_PRESSURE)])
def test_warning_failure_is_detected_but_does_not_fake_critical(field,code):
    m,*_=golden_bundle();r=qualify_failures(m.bundle_hash,**{field:False});assert any(f.code is code and f.detected for f in r.findings)
def test_replay_sorts_known_time_and_is_deterministic():
    req=[golden_request(3),golden_request(1),golden_request(2)];a,ha=replay(make_host(),req);b,hb=replay(make_host(),list(reversed(req)));assert [d.request_id for d in a]==['req:1','req:2','req:3'];assert ha==hb
def test_prefix_stability():
    assert assert_prefix_stable(make_host,[golden_request(i) for i in range(1,5)])
def test_future_suffix_does_not_change_prefix_decisions():
    base=[golden_request(i) for i in range(1,4)];full=base+[golden_request(99)];a,_=replay(make_host(),base);b,_=replay(make_host(),full);assert [d.decision_hash for d in a]==[d.decision_hash for d in b[:3]]
