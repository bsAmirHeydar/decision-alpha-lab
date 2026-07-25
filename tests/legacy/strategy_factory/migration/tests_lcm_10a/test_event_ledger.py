from .conftest import j
def test_events_are_contiguous_and_authority_negative():
 d=j('events/treatment_inventory_event_ledger.json');assert [x['sequence'] for x in d['events']]==list(range(1,d['event_count']+1));assert all(not x['authority_created'] for x in d['events'])
