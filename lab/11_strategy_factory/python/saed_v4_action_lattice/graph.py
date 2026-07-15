from __future__ import annotations
from collections import defaultdict, deque
from typing import Any
from .errors import ContractError

def validate_dag(nodes:list[dict[str,Any]],edges:list[dict[str,Any]])->list[str]:
    ids={n['node_id'] for n in nodes};ind={i:0 for i in ids};adj=defaultdict(list)
    for e in edges:
        s,t=e['source_node_id'],e['target_node_id']
        if s not in ids or t not in ids: raise ContractError('dangling lattice edge')
        if s==t: raise ContractError('self-loop forbidden')
        adj[s].append(t);ind[t]+=1
    q=deque(sorted(i for i,d in ind.items() if d==0));order=[]
    while q:
        x=q.popleft();order.append(x)
        for y in sorted(adj[x]):
            ind[y]-=1
            if ind[y]==0:q.append(y)
    if len(order)!=len(ids): raise ContractError('action lattice cycle detected')
    return order

def validate_atomic_edges(nodes:list[dict[str,Any]],edges:list[dict[str,Any]])->None:
    by={n['node_id']:n for n in nodes}
    for e in edges:
        if e['edge_kind']!='atomic_parameter_step': continue
        a,b=by[e['source_node_id']],by[e['target_node_id']];keys=set(a['domain_indices'])|set(b['domain_indices'])
        diffs=[k for k in keys if a['domain_indices'].get(k)!=b['domain_indices'].get(k)]
        if len(diffs)!=1: raise ContractError('non-atomic parameter edge')
        k=diffs[0]
        if b['domain_indices'][k]-a['domain_indices'][k]!=1: raise ContractError('non-adjacent or reverse atomic edge')
