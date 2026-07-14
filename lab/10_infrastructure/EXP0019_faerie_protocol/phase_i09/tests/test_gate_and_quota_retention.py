from fp_i08_weekly.enums import GateEligibility
from fp_i09_ledger.identity import build_contender
from fp_i09_ledger.arbiter import resolve_pair_session
from conftest import signal,gate,eligible

def test_ww_suppressed_not_quota_contender(qkey):
    s=signal(); g=gate(s,GateEligibility.SUPPRESSED); c=build_contender(s,qkey,eligible(s,g)); d=resolve_pair_session(qkey,(c,),evaluated_utc_ms=s.confirmation_close_utc_ms)
    assert not d.winner_signal_id and s.signal_id in d.suppressed_signal_ids
def test_blocked_signal_retained(qkey):
    s=signal(); c=build_contender(s,qkey,eligible(s,data_ready=False)); d=resolve_pair_session(qkey,(c,),evaluated_utc_ms=s.confirmation_close_utc_ms)
    assert s.signal_id in d.blocked_signal_ids
def test_ww_direct_setup_competes(qkey):
    from fp_i02_kernel.enums import RelationCode
    a=signal(0,relation=RelationCode.WW); b=signal(1,relation=RelationCode.AL,hunt=a.first_hunt_minute_utc_ms+60_000)
    ca=build_contender(a,qkey,eligible(a)); cb=build_contender(b,qkey,eligible(b)); d=resolve_pair_session(qkey,(cb,ca),evaluated_utc_ms=b.confirmation_close_utc_ms)
    assert d.winner_signal_id==a.signal_id
