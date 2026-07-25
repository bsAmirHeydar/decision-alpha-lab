from __future__ import annotations
from .canonical import content_hash,seal

def graph(items:dict)->dict:
    nodes=[]; edges=[]
    for kind,obj in sorted(items.items()):
        oid=next((obj[k] for k in sorted(obj) if k.endswith("_id")),kind); oh=next((obj[k] for k in sorted(obj) if k.endswith("_hash")),content_hash(obj))
        nodes.append({"node_id":f"{kind}:{oid}","kind":kind,"content_hash":oh})
    order=list(sorted(items))
    for a,b in zip(order,order[1:]): edges.append({"source":f"{a}:{next((items[a][k] for k in sorted(items[a]) if k.endswith('_id')),a)}","target":f"{b}:{next((items[b][k] for k in sorted(items[b]) if k.endswith('_id')),b)}","relation":"derived_before"})
    return seal({"phase":"SAED_V4_34","nodes":nodes,"edges":edges,"node_count":len(nodes),"edge_count":len(edges),"acyclic":True,"complete":True,"research_only":True},"v434_provenance","graph_id","graph_hash")
