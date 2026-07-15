from .canonical import content_hash, stable_id

def semantic_diff(left:dict,right:dict)->dict:
    keys=sorted(set(left)|set(right)); changes=[]
    for k in keys:
        if left.get(k)!=right.get(k): changes.append({"field":k,"left":left.get(k),"right":right.get(k)})
    payload={"phase":"SAED_V4_10","change_count":len(changes),"changes":changes,"semantically_equal":not changes}
    payload['diff_id']=stable_id('v410diff',payload);payload['diff_hash']=content_hash(payload);return payload
