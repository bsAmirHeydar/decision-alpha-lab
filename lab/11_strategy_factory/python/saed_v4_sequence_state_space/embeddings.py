from __future__ import annotations
from .errors import IntegrityError,ContractError
from .canonical import content_hash
from .numerics import mean_vec

class FrozenEmbeddingTable:
    def __init__(self,checkpoint:dict,expected_hash:str):
        if checkpoint.get('checkpoint_hash')!=expected_hash: raise IntegrityError('frozen encoder checkpoint hash mismatch')
        self.checkpoint_hash=expected_hash;self.dimension=int(checkpoint['dimension']);self.embeddings={str(k):tuple(map(float,v)) for k,v in checkpoint['embeddings'].items()}
        if any(len(v)!=self.dimension for v in self.embeddings.values()): raise ContractError('embedding width mismatch')
    def token(self,t:str)->tuple[float,...]:
        if t in self.embeddings:return self.embeddings[t]
        return tuple(0.0 for _ in range(self.dimension))
    def stream(self,tokens)->tuple[float,...]:
        rows=[self.token(str(t)) for t in tokens]
        return mean_vec(rows) if rows else tuple(0.0 for _ in range(self.dimension))
    def binding(self)->dict:
        material={'checkpoint_hash':self.checkpoint_hash,'dimension':self.dimension,'vocabulary_size':len(self.embeddings),'frozen':True,'trainable_parameters':0}
        return {**material,'binding_hash':content_hash(material)}
