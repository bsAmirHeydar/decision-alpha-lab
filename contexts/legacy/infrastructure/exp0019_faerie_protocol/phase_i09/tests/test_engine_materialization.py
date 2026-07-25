from fp_i09_ledger.engine import LedgerEngine
from fp_i09_ledger.enums import LedgerDisposition
from conftest import signal,gate,eligible

def test_engine_winner_and_suppressed(config,qkey):
    e=LedgerEngine(config); a=signal(0); b=signal(1,hunt=a.first_hunt_minute_utc_ms+60_000)
    e.ingest(b,gate(b),eligible(b),qkey,b.confirmation_close_utc_ms); e.ingest(a,gate(a),eligible(a),qkey,a.confirmation_close_utc_ms+600_000)
    snap=e.snapshot(a.confirmation_close_utc_ms+660_000); by={r.signal.signal_id:r for r in snap.records}
    assert by[a.signal_id].disposition is LedgerDisposition.QUOTA_WINNER
    assert by[b.signal_id].disposition is LedgerDisposition.SUPPRESSED_BY_QUOTA
    assert len(snap.signal_index)==2 and snap.chain_head_hash
def test_indexes_are_canonical(config,qkey):
    e=LedgerEngine(config); s=signal(); e.ingest(s,gate(s),eligible(s),qkey,s.confirmation_close_utc_ms); snap=e.snapshot(s.confirmation_close_utc_ms)
    assert snap.session_index[0][0]==s.owner_session_id and snap.relation_index[0][0]==s.relation.value
def test_duplicate_signal_has_one_record(config,qkey):
    e=LedgerEngine(config); s=signal(); e.ingest(s,gate(s),eligible(s),qkey,s.confirmation_close_utc_ms); e.ingest(s,gate(s),eligible(s),qkey,s.confirmation_close_utc_ms+60_000); assert len(e.snapshot(s.confirmation_close_utc_ms+60_000).records)==1
def test_seal_marks_final(config,qkey):
    e=LedgerEngine(config); s=signal(); e.ingest(s,gate(s),eligible(s),qkey,s.confirmation_close_utc_ms); d=e.seal(qkey,s.confirmation_close_utc_ms+60_000); assert d.reservation.finality.value=='FINAL'
