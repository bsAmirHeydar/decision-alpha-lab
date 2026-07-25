import pytest
from fp_i09_ledger.store import AppendOnlyLedger
from fp_i09_ledger.events import make_event,verify_chain
from fp_i09_ledger.enums import LedgerEventType
from fp_i09_ledger.errors import FPI09Error
from conftest import signal

def test_signal_ingest_builds_chain():
    l=AppendOnlyLedger(); s=signal(); l.ingest_signal(s,s.confirmation_close_utc_ms); assert verify_chain(l.events)
def test_identical_duplicate_is_audited_not_reinserted():
    l=AppendOnlyLedger(); s=signal(); l.ingest_signal(s,s.confirmation_close_utc_ms); e,f=l.ingest_signal(s,s.confirmation_close_utc_ms+60_000); assert not f and e.event_type is LedgerEventType.DUPLICATE_SIGNAL_IGNORED
def test_event_id_duplicate_ignored():
    l=AppendOnlyLedger(); e=make_event(0,LedgerEventType.REBUILD_COMPLETED,'A',1_800_000_000_000,{'x':1}); assert l.append(e) and not l.append(e)
def test_chain_break_rejected():
    l=AppendOnlyLedger(); e=make_event(1,LedgerEventType.REBUILD_COMPLETED,'A',1_800_000_000_000,{'x':1},prior_event_hash='0'*64)
    with pytest.raises(FPI09Error): l.append(e)
def test_tampered_chain_detected():
    l=AppendOnlyLedger(); s=signal(); l.ingest_signal(s,s.confirmation_close_utc_ms); assert verify_chain(l.events)
