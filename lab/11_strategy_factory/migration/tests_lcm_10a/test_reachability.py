from .conftest import j,jl
def test_broker_hits_are_reachable_or_explicit_unknown():
 rr=jl('reachability/broker_api_reachability.jsonl');u=jl('unknowns/execution_unknown_queue.jsonl');subjects={x['subject_id'] for x in u};assert len(rr)==1408;assert all(x['reachability_state']=='REACHABLE_FROM_STATIC_ENTRY' or x['reachability_id'] in subjects for x in rr)
