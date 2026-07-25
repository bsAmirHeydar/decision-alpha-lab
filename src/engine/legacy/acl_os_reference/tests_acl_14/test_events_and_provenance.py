from tools.strategy_factory.acl_os.acl_14.events import build_event_ledger,verify_event_ledger
def test_event_chain():
    d=build_event_ledger('RUN','2026-07-18T10:00:00Z',[('A',{}),('B',{})]); assert verify_event_ledger(d)
def test_event_tamper_detected():
    d=build_event_ledger('RUN','2026-07-18T10:00:00Z',[('A',{}),('B',{})]); d['events'][1]['event_type']='X'; assert not verify_event_ledger(d)
def test_no_authority_in_events():
    d=build_event_ledger('RUN','2026-07-18T10:00:00Z',[('A',{})]); assert all(not e['pilot_execution_authority'] and not e['live_order_authority'] for e in d['events'])
