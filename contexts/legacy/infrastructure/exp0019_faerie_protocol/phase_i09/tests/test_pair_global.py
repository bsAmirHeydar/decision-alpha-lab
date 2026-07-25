from fp_i09_ledger.engine import LedgerEngine
from conftest import signal,gate,eligible

def test_both_symbols_share_one_quota(config,qkey):
    e=LedgerEngine(config); a=signal(0,hunter='ES',protected='NQ'); b=signal(1,hunter='NQ',protected='ES',hunt=a.first_hunt_minute_utc_ms+60_000)
    e.ingest(a,gate(a),eligible(a),qkey,a.confirmation_close_utc_ms); d=e.ingest(b,gate(b),eligible(b),qkey,b.confirmation_close_utc_ms); assert d.winner_signal_id==a.signal_id and len(d.suppressed_signal_ids)==1
def test_different_sessions_get_different_winners(config,qkey):
    from fp_i09_ledger.identity import build_quota_key
    e=LedgerEngine(config); a=signal(0); q2=build_quota_key('EPOCH-1','NYDAY-2026-09-08','PAIR-ES-NQ','NYDAY-2026-09-08:L','L'); b=signal(1,session='NYDAY-2026-09-08:L')
    assert e.ingest(a,gate(a),eligible(a),qkey,a.confirmation_close_utc_ms).winner_signal_id==a.signal_id
    assert e.ingest(b,gate(b),eligible(b),q2,b.confirmation_close_utc_ms).winner_signal_id==b.signal_id
