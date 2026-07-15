from __future__ import annotations
from .canonical import content_hash, stable_id

def semantic_diff(left:dict,right:dict)->dict:
    ignored={'checkpoint_id','checkpoint_hash'}
    changes=[]
    keys=sorted((set(left)|set(right))-ignored)
    for key in keys:
        if left.get(key)!=right.get(key):
            changes.append({"field":key,"left_hash":content_hash(left.get(key)),"right_hash":content_hash(right.get(key))})
    payload={"phase":"SAED_V4_11","left_checkpoint_hash":left.get('checkpoint_hash'),"right_checkpoint_hash":right.get('checkpoint_hash'),"changes":changes,"change_count":len(changes),"decision_equivalent":not changes}
    payload['diff_id']=stable_id('v411diff',payload);payload['diff_hash']=content_hash(payload);return payload
