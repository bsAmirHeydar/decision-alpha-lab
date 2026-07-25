from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash,stable_id
from .errors import ContractError,IntegrityError,TopologyError,BudgetError,ContaminationError
from .temporal import assert_known_time
from .features import node_features,distilled_state

FORBIDDEN_KEYS={'outcome','label','pnl','profit','return','mae','mfe','fill_price','realized','future','target'}
def _scan_forbidden(value,path='root'):
    if isinstance(value,dict):
        for k,v in value.items():
            if str(k).lower() in FORBIDDEN_KEYS: raise ContaminationError(f'forbidden graph input key {path}.{k}')
            _scan_forbidden(v,f'{path}.{k}')
    elif isinstance(value,list):
        for i,v in enumerate(value):_scan_forbidden(v,f'{path}[{i}]')

def compile_graph(graph:dict,snapshots_doc:dict,distillation:dict,spec,cutoff:str)->dict:
    _scan_forbidden(graph)
    if graph.get('known_as_of')!=cutoff: raise ContractError('cutoff must equal frozen graph known_as_of')
    nodes=[];seen=set();snapshots=snapshots_doc.get('snapshots',[])
    if not snapshots: raise IntegrityError('no frozen sequence snapshots')
    dstates=[distilled_state(s,distillation) for s in snapshots]
    for raw in sorted(graph.get('nodes',[]),key=lambda x:x['node_id']):
        if raw['node_id'] in seen: raise TopologyError('duplicate node id')
        seen.add(raw['node_id']);assert_known_time(raw['event_time'],raw['known_time'],cutoff)
        idx=int(content_hash(raw['node_id'])[:8],16)%len(dstates)
        nodes.append({'node_id':raw['node_id'],'kind':raw.get('kind','unknown'),'semantic_key':raw.get('semantic_key',''),
                      'event_time':raw['event_time'],'known_time':raw['known_time'],'quality':float(raw.get('quality',0.0)),
                      'sequence_state':list(dstates[idx]),'feature':list(node_features(raw,spec.input_dim,dstates[idx])),
                      'split':'train' if int(content_hash(raw['node_id'])[:2],16)%5 else 'eval','source_node_hash':raw['node_hash']})
    if len(nodes)>spec.max_nodes: raise BudgetError('node budget exceeded')
    node_ids=set(x['node_id'] for x in nodes);hyperedges=[];relations=set();pair_map=defaultdict(set)
    for e in sorted(graph.get('edges',[]),key=lambda x:x['edge_id']):
        assert_known_time(e['event_time_end'],e['known_time'],cutoff)
        members=tuple(sorted(e['member_node_ids']))
        if len(members)<2 or not set(members).issubset(node_ids): raise TopologyError('dangling or unary hyperedge')
        if len(members)>spec.max_clique_degree: members=members[:spec.max_clique_degree]
        rel=str(e['relation_kind']);relations.add(rel)
        hyperedges.append({'edge_id':e['edge_id'],'relation_kind':rel,'member_node_ids':list(members),'known_time':e['known_time'],'quality':float(e.get('quality',0.0)),'source_edge_hash':e['edge_hash']})
        for i,a in enumerate(members):
            for b in members[i+1:]:
                pair_map[(a,b)].add(rel);pair_map[(b,a)].add(rel)
    if len(hyperedges)>spec.max_hyperedges: raise BudgetError('hyperedge budget exceeded')
    pair_edges=[{'source':a,'target':b,'relation_kinds':sorted(rs)} for (a,b),rs in sorted(pair_map.items())]
    degree={n['node_id']:0 for n in nodes}
    for p in pair_edges:degree[p['source']]+=1
    payload={'phase':'SAED_V4_13','source_graph_id':graph['graph_id'],'source_graph_hash':graph['graph_hash'],'known_as_of':cutoff,
             'nodes':nodes,'hyperedges':hyperedges,'pair_edges':pair_edges,'relation_kinds':sorted(relations),'degree':degree,
             'sequence_distillation_hash':distillation['distillation_hash'],'frozen':True}
    payload['compiled_graph_hash']=content_hash(payload);payload['compiled_graph_id']=stable_id('modelgraph',payload)
    return payload

def adjacency(graph:dict):
    out=defaultdict(list)
    for e in graph['pair_edges']:
        out[e['source']].append((e['target'],tuple(e['relation_kinds'])))
    return {k:tuple(sorted(v)) for k,v in out.items()}
def incidence(graph:dict):
    out=defaultdict(list)
    for e in graph['hyperedges']:
        for n in e['member_node_ids']:out[n].append(e['edge_id'])
    return {k:tuple(sorted(v)) for k,v in out.items()}
