from __future__ import annotations
from .canonical import content_hash,stable_id,merkle_root

def build_partition_manifest(lattice:dict,partition_count:int)->dict:
    parts=[{'partition_id':i,'node_ids':[]} for i in range(partition_count)]
    for n in sorted(lattice['nodes'],key=lambda n:n['node_id']):
        parts[int(n['node_hash'][:16],16)%partition_count]['node_ids'].append(n['node_id'])
    for p in parts:p['partition_hash']=content_hash({'partition_id':p['partition_id'],'node_ids':p['node_ids']})
    seed={'lattice_hash':lattice['lattice_hash'],'partition_count':partition_count,'partition_hashes':[p['partition_hash'] for p in parts],'partition_root':merkle_root(p['partition_hash'] for p in parts)}
    return {'manifest_id':stable_id('latticepartition',seed),'manifest_hash':content_hash(seed),**seed,'partitions':parts,'assignment_method':'sha256_prefix_modulo'}
