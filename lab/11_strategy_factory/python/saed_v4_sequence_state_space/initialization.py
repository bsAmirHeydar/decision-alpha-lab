from __future__ import annotations
from .canonical import hash_signed,content_hash

def vector(seed:str,n:int,scale:float=0.2): return tuple(hash_signed(f'{seed}:{i}')*scale for i in range(n))
def matrix(seed:str,rows:int,cols:int,scale:float=0.2): return tuple(vector(f'{seed}:{r}',cols,scale) for r in range(rows))
def initializer_receipt(candidate_id:str,seed:int,input_dim:int,state_dim:int)->dict:
    material={'candidate_id':candidate_id,'seed':seed,'input_dim':input_dim,'state_dim':state_dim,'algorithm':'sha256_counter_signed_v1','scale':0.2}
    return {**material,'initializer_hash':content_hash(material)}
