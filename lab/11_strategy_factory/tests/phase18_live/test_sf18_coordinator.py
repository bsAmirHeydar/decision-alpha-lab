from dataclasses import replace
from strategy_factory_live import *
from strategy_factory_live.examples import reference_bundle

def test_dry_run_checks_but_never_sends():
    release,auth,policy,intent,account,quote=reference_bundle(); broker=DeterministicDryRunBroker()
    e=LiveExecutionCoordinator("run",LiveMode.DRY_RUN,release,auth,policy,broker)
    d=e.submit(intent,account,quote,quote.time_utc_msc)
    assert d.decision==LiveDecision.CHECK_ONLY and len(broker.checked)==1 and len(broker.sent)==0
    assert e.ledger.validate_chain() and e.report(quote.time_utc_msc+1).checks_accepted==1

def test_micro_live_requires_explicit_arm_and_consumes_one_shot():
    release,auth,policy,intent,account,quote=reference_bundle()
    auth=replace(auth,mode=LiveMode.MICRO_LIVE,authorization_hash=""); auth=replace(auth,authorization_hash=auth.derived_hash())
    broker=DeterministicDryRunBroker(); e=LiveExecutionCoordinator("run",LiveMode.MICRO_LIVE,release,auth,policy,broker)
    blocked=e.submit(intent,account,quote,quote.time_utc_msc)
    assert blocked.reject_reason==LiveRejectReason.AUTHORIZATION_MISSING and len(broker.sent)==0
    # use a new intent because rejected identities are immutable
    intent2=replace(intent,intent_id="intent-2",intent_hash="intent-hash-2")
    assert e.arm_micro_live(quote.time_utc_msc)
    accepted=e.submit(intent2,account,quote,quote.time_utc_msc+1)
    assert accepted.decision==LiveDecision.ACCEPTED and len(broker.sent)==1
    assert e.authorization_state==AuthorizationState.CONSUMED
    intent3=replace(intent,intent_id="intent-3",intent_hash="intent-hash-3")
    blocked2=e.submit(intent3,account,quote,quote.time_utc_msc+2)
    assert blocked2.reject_reason==LiveRejectReason.AUTHORIZATION_CONSUMED and len(broker.sent)==1

def test_duplicate_replay_is_idempotent():
    release,auth,policy,intent,account,quote=reference_bundle(); broker=DeterministicDryRunBroker()
    e=LiveExecutionCoordinator("run",LiveMode.DRY_RUN,release,auth,policy,broker)
    a=e.submit(intent,account,quote,quote.time_utc_msc); b=e.submit(intent,account,quote,quote.time_utc_msc+1)
    assert a.request_id==b.request_id and b.reject_reason==LiveRejectReason.IDEMPOTENT_REPLAY and len(broker.checked)==1

def test_check_rejection_opens_circuit_after_threshold():
    release,auth,policy,intent,account,quote=reference_bundle(); broker=DeterministicDryRunBroker(check_retcode=10006)
    e=LiveExecutionCoordinator("run",LiveMode.DRY_RUN,release,auth,policy,broker)
    for n in range(2):
        x=replace(intent,intent_id=f"i{n}",intent_hash=f"h{n}")
        assert e.submit(x,account,quote,quote.time_utc_msc+n).decision==LiveDecision.REJECT
    assert e.circuit.state==CircuitState.OPEN
