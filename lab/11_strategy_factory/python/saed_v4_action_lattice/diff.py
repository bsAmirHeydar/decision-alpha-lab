from __future__ import annotations
from .canonical import content_hash,stable_id

def semantic_diff(left:dict,right:dict)->dict:
    added=sorted(set(n['node_id'] for n in right['nodes'])-set(n['node_id'] for n in left['nodes']))
    removed=sorted(set(n['node_id'] for n in left['nodes'])-set(n['node_id'] for n in right['nodes']))
    changed=[]
    by_l={n['node_id']:n for n in left['nodes']};by_r={n['node_id']:n for n in right['nodes']}
    for k in sorted(set(by_l)&set(by_r)):
        if by_l[k]['node_hash']!=by_r[k]['node_hash']:changed.append(k)
    cls='identical' if not (added or removed or changed) and left['lattice_hash']==right['lattice_hash'] else 'semantic'
    seed={'left_lattice_hash':left['lattice_hash'],'right_lattice_hash':right['lattice_hash'],'added_node_ids':added,'removed_node_ids':removed,'changed_node_ids':changed,'diff_class':cls}
    return {'diff_id':stable_id('latticediff',seed),'diff_hash':content_hash(seed),**seed}
