from fp_i09_ledger.identity import build_contender
from fp_i09_ledger.arbiter import resolve_pair_session
from conftest import signal,eligible

def c(s,q): return build_contender(s,q,eligible(s))
def test_late_earlier_hunt_supersedes_provisional(qkey):
    later=signal(1,hunt=1_800_000_600_000); d1=resolve_pair_session(qkey,(c(later,qkey),),evaluated_utc_ms=later.confirmation_close_utc_ms)
    earlier=signal(0,hunt=1_800_000_000_000); d2=resolve_pair_session(qkey,(c(later,qkey),c(earlier,qkey)),evaluated_utc_ms=later.confirmation_close_utc_ms+60_000,prior_reservation=d1.reservation)
    assert d2.winner_signal_id==earlier.signal_id and d2.reservation.generation==2 and d2.reservation.prior_reservation_id==d1.reservation.reservation_id
def test_same_winner_keeps_generation(qkey):
    s=signal(); d1=resolve_pair_session(qkey,(c(s,qkey),),evaluated_utc_ms=s.confirmation_close_utc_ms); d2=resolve_pair_session(qkey,(c(s,qkey),),evaluated_utc_ms=s.confirmation_close_utc_ms+60_000,prior_reservation=d1.reservation)
    assert d2.reservation.generation==1
def test_prior_reservation_does_not_consume(qkey):
    s=signal(); d=resolve_pair_session(qkey,(c(s,qkey),),evaluated_utc_ms=s.confirmation_close_utc_ms); assert d.reservation.consumption_policy.value=='UNSET'
