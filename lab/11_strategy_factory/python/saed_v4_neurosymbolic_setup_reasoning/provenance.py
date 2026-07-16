from __future__ import annotations
from .canonical import content_hash

def graph(upstream_hash,artifacts):
    nodes=[{'node_id':'v4_18_handoff','node_type':'upstream','content_hash':upstream_hash}]+[{'node_id':k,'node_type':'v4_19_artifact','content_hash':content_hash(v)} for k,v in sorted(artifacts.items())]
    edges=[{'source':'v4_18_handoff','target':n['node_id'],'relation':'derived_from'} for n in nodes[1:]]
    return {'nodes':nodes,'edges':edges,'graph_hash':content_hash({'nodes':nodes,'edges':edges})}
