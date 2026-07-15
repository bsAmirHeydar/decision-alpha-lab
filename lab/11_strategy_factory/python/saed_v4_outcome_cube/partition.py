from __future__ import annotations
from .canonical import content_hash,stable_id

def partition_nodes(lattice,count:int):
    if count<=0:raise ValueError('partition count')
    parts=[[] for _ in range(count)]
    for i,node in enumerate(sorted(lattice['nodes'],key=lambda n:n['node_id'])):parts[i%count].append(node['node_id'])
    payload={'source_lattice_hash':lattice['lattice_hash'],'partition_count':count,'partitions':[{'partition_id':i,'node_ids':p,'node_count':len(p)} for i,p in enumerate(parts)],'merge_order':'node_id_ascending'};payload['manifest_id']=stable_id('cubepartition',payload);payload['manifest_hash']=content_hash(payload);return payload
