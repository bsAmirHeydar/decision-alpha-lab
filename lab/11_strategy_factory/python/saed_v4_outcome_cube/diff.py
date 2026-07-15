from __future__ import annotations
from .canonical import content_hash,stable_id

def semantic_diff(left,right):
    l={r.node_id:r for r in left.rows};r={x.node_id:x for x in right.rows};changed=[]
    for node in sorted(set(l)|set(r)):
        if node not in l:changed.append({'node_id':node,'change':'added'})
        elif node not in r:changed.append({'node_id':node,'change':'removed'})
        elif l[node].row_hash!=r[node].row_hash:changed.append({'node_id':node,'change':'modified','left_row_hash':l[node].row_hash,'right_row_hash':r[node].row_hash})
    payload={'left_cube_hash':left.cube_hash,'right_cube_hash':right.cube_hash,'changed_rows':changed,'changed_count':len(changed),'ranking_semantics':'none'};payload['diff_id']=stable_id('cubediff',payload);payload['diff_hash']=content_hash(payload);return payload
