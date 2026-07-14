from fp_i09_ledger.engine import LedgerEngine
from fp_i09_ledger.rebuild import assert_semantic_parity
from conftest import signal,gate,eligible

def build(config,qkey,items):
    e=LedgerEngine(config)
    for s in items: e.ingest(s,gate(s),eligible(s),qkey,s.confirmation_close_utc_ms+600_000)
    return e.snapshot(max(s.confirmation_close_utc_ms for s in items)+900_000)

def test_reversed_arrival_order_has_same_semantic_winner(config,qkey):
    early=signal(0); late=signal(1,hunt=early.first_hunt_minute_utc_ms+60_000)
    assert assert_semantic_parity(build(config,qkey,(early,late)),build(config,qkey,(late,early)))
