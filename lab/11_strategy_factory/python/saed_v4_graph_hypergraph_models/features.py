from __future__ import annotations
from .canonical import hash_signed,content_hash

def _hash_vector(seed:str,n:int)->tuple[float,...]: return tuple(hash_signed(f'{seed}|{i}') for i in range(n))
def distilled_state(snapshot:dict,distillation:dict)->tuple[float,...]:
    hidden=snapshot['hidden'];proj=distillation['projection']
    return tuple(sum(float(hidden[j])*float(row[j]) for j in range(min(len(hidden),len(row)))) for row in proj)
def node_features(node:dict,dim:int,sequence_state:tuple[float,...])->tuple[float,...]:
    base=[float(node.get('quality',0.0)),1.0 if node.get('masked') else 0.0,1.0 if node.get('missing') else 0.0,
          min(1.0,len(node.get('source_hashes',[]))/8.0),min(1.0,len(node.get('attributes',{}))/12.0)]
    base += list(sequence_state)
    seed=content_hash({'node_id':node['node_id'],'kind':node.get('kind'),'semantic_key':node.get('semantic_key'),'attributes':node.get('attributes',{})})
    base += list(_hash_vector(seed,max(0,dim-len(base))))
    return tuple(base[:dim])
def relation_embedding(kind:str,dim:int)->tuple[float,...]: return _hash_vector('relation|'+kind,dim)
