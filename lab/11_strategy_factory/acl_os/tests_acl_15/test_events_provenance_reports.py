from tools.strategy_factory.acl_os.acl_15.events import build_event_ledger,verify_event_ledger
def test_event_chain_valid():
 l=build_event_ledger('RUN','2026-07-18T11:00:00Z',[('A',{}),('B',{})]); assert verify_event_ledger(l)
def test_event_chain_tamper_detected():
 l=build_event_ledger('RUN','2026-07-18T11:00:00Z',[('A',{}),('B',{})]); l['events'][1]['previous_event_digest']='x'; assert not verify_event_ledger(l)
def test_event_authorities_false():
 l=build_event_ledger('RUN','2026-07-18T11:00:00Z',[('A',{})]); assert not any(l['events'][0][k] for k in ['pilot_execution_authority','runtime_generation_authority','live_order_authority','capital_authority'])
