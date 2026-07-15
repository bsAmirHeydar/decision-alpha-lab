from __future__ import annotations
from .canonical import content_hash,stable_id

def build_exposure(nodes,rows):
    expected=sorted(n['node_id'] for n in nodes);observed=sorted(r.node_id for r in rows);missing=sorted(set(expected)-set(observed));duplicates=sorted(x for x in set(observed) if observed.count(x)>1);unexpected=sorted(set(observed)-set(expected))
    status_counts={}
    for r in rows:status_counts[r.status]=status_counts.get(r.status,0)+1
    payload={'expected_node_count':len(expected),'observed_row_count':len(observed),'expected_node_ids':expected,'observed_node_ids':observed,'missing_node_ids':missing,'duplicate_node_ids':duplicates,'unexpected_node_ids':unexpected,'status_counts':dict(sorted(status_counts.items())),'complete':not(missing or duplicates or unexpected)}
    payload['ledger_id']=stable_id('outcomeexposure',payload);payload['ledger_hash']=content_hash(payload);return payload
