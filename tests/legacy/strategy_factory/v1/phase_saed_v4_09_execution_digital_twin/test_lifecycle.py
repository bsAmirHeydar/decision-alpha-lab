from .helpers import built

def test_event_hash_chain_is_complete():
    *_,twin=built()
    for row in twin['rows']:
        prev='0'*64
        for i,event in enumerate(row['lifecycle_events']):
            assert event['sequence']==i and event['previous_event_hash']==prev;prev=event['event_hash']

def test_lifecycle_budget_is_respected():
    _,_,profile,twin=built();assert all(len(r['lifecycle_events'])<=profile.maximum_lifecycle_events_per_row for r in twin['rows'])
