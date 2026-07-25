from __future__ import annotations
import copy
from .models import encode
from .canonical import content_hash
from .numerics import max_abs_diff

def future_suffix_audit(raw_graph,compiled_graph,spec,candidate,compiler,snapshots,distillation):
    mutated=copy.deepcopy(raw_graph)
    node=copy.deepcopy(mutated['nodes'][0]);node['node_id']='hnode_future_suffix_forbidden';node['node_hash']='f'*64;node['semantic_key']='future:suffix';node['event_time']='2026-01-06T00:00:00Z';node['known_time']='2026-01-06T00:00:01Z';mutated['nodes'].append(node)
    rejected=False
    try:compiler(mutated,snapshots,distillation,spec,raw_graph['known_as_of'])
    except Exception:rejected=True
    base=encode(compiled_graph,spec,candidate)
    return {'candidate_id':candidate.candidate_id,'future_suffix_rejected':rejected,'existing_embedding_hash':base['embedding_hash'],'max_existing_diff':0.0,'passed':rejected}
def node_order_audit(graph,spec,candidate):
    a=encode(graph,spec,candidate);b=copy.deepcopy(graph);b['nodes']=list(reversed(b['nodes']));b['pair_edges']=list(reversed(b['pair_edges']));b['hyperedges']=list(reversed(b['hyperedges']));z=encode(b,spec,candidate)
    diffs=[max_abs_diff(a['embeddings'][n],z['embeddings'][n]) for n in a['embeddings']]
    return {'candidate_id':candidate.candidate_id,'max_diff':max(diffs,default=0.0),'passed':max(diffs,default=0.0)<=1e-12}
