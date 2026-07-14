from fp_i02_kernel.enums import RelationCode,Direction
from fp_i09_ledger.identity import build_contender
from fp_i09_ledger.arbiter import resolve_pair_session,assert_consumption_forbidden
from fp_i09_ledger.enums import SessionSealState,ReservationFinality
from fp_i09_ledger.errors import FPI09Error
from conftest import signal,gate,eligible
import pytest

def c(s,q): return build_contender(s,q,eligible(s))
def test_earliest_hunt_wins(qkey):
    a=signal(0,hunt=1_800_000_000_000); b=signal(1,hunt=1_800_000_060_000)
    d=resolve_pair_session(qkey,(c(b,qkey),c(a,qkey)),evaluated_utc_ms=1_800_001_020_000)
    assert d.winner_signal_id==a.signal_id and b.signal_id in d.suppressed_signal_ids
def test_confirmation_is_secondary_tiebreak(qkey):
    h=1_800_000_000_000; a=signal(0,hunt=h,confirm=h+600_000); b=signal(1,hunt=h,confirm=h+300_000)
    assert resolve_pair_session(qkey,(c(a,qkey),c(b,qkey)),evaluated_utc_ms=h+900_000).winner_signal_id==b.signal_id
def test_relation_is_tertiary_tiebreak(qkey):
    h=1_800_000_000_000; co=h+300_000; a=signal(0,relation=RelationCode.WW,hunt=h,confirm=co); b=signal(1,relation=RelationCode.AL,hunt=h,confirm=co)
    assert resolve_pair_session(qkey,(c(a,qkey),c(b,qkey)),evaluated_utc_ms=co).winner_signal_id==b.signal_id
def test_direction_tiebreak(qkey):
    h=1_800_000_000_000; co=h+300_000; a=signal(0,direction=Direction.BEARISH,hunt=h,confirm=co); b=signal(1,direction=Direction.BULLISH,hunt=h,confirm=co)
    assert resolve_pair_session(qkey,(c(a,qkey),c(b,qkey)),evaluated_utc_ms=co).winner_signal_id==b.signal_id
def test_duplicate_contender_collapses(qkey):
    s=signal(); x=c(s,qkey); d=resolve_pair_session(qkey,(x,x),evaluated_utc_ms=s.confirmation_close_utc_ms); assert len(d.contender_ids)==1
def test_sealed_reservation_is_final(qkey):
    s=signal(); d=resolve_pair_session(qkey,(c(s,qkey),),evaluated_utc_ms=s.confirmation_close_utc_ms,seal_state=SessionSealState.SEALED); assert d.reservation.finality is ReservationFinality.FINAL
def test_open_reservation_is_provisional(qkey):
    s=signal(); d=resolve_pair_session(qkey,(c(s,qkey),),evaluated_utc_ms=s.confirmation_close_utc_ms); assert d.reservation.finality is ReservationFinality.PROVISIONAL
def test_consumption_forbidden():
    with pytest.raises(FPI09Error): assert_consumption_forbidden()
