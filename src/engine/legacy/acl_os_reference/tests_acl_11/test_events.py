from src.engine.tooling.strategy_factory.acl_os.acl_11.events import build_event_ledger,verify_event_ledger
def test_event_chain():
    l=build_event_ledger('R','2026-07-18T04:00:00Z',[('A',{}),('B',{})]); assert verify_event_ledger(l)
def test_event_tamper_detected():
    l=build_event_ledger('R','2026-07-18T04:00:00Z',[('A',{}),('B',{})]); l['events'][1]['payload']['x']=1; assert not verify_event_ledger(l)
