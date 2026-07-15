from __future__ import annotations
import math
from .canonical import hash_signed, content_hash, stable_id
from .errors import TrainingError, CheckpointError

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sigmoid(x):
    x=max(-30.0,min(30.0,x))
    return 1.0/(1.0+math.exp(-x))
def norm(v): return math.sqrt(sum(x*x for x in v))
def cosine(a,b):
    d=norm(a)*norm(b)
    return 0.0 if d==0 else dot(a,b)/d

def _normalise(v):
    n=norm(v)
    return [0.0 for _ in v] if n==0 else [x/n for x in v]

class ReferenceEmbeddingEncoder:
    def __init__(self,vocabulary:list[str],dimension:int,seed:int,embeddings:dict[str,list[float]]|None=None):
        self.vocabulary=tuple(vocabulary);self.dimension=dimension;self.seed=seed
        if embeddings is None:
            scale=1.0/math.sqrt(dimension)
            self.embeddings={t:[hash_signed(f'{seed}|{t}|{i}')*scale for i in range(dimension)] for t in self.vocabulary}
        else:
            if set(embeddings)!=set(vocabulary): raise CheckpointError('checkpoint vocabulary mismatch')
            self.embeddings={t:[float(x) for x in embeddings[t]] for t in self.vocabulary}
            if any(len(v)!=dimension for v in self.embeddings.values()): raise CheckpointError('checkpoint dimension mismatch')
    def encode(self,tokens:list[str]|tuple[str,...])->list[float]:
        rows=[self.embeddings[t] for t in tokens if t in self.embeddings and not t.startswith('[')]
        if not rows: return [0.0]*self.dimension
        return _normalise([sum(r[i] for r in rows)/len(rows) for i in range(self.dimension)])
    def train_pair(self,anchor:str,positive:str,negative_tokens:list[str]|tuple[str,...],learning_rate:float,weight:float)->float:
        if anchor not in self.embeddings or positive not in self.embeddings: raise TrainingError('unknown training token')
        loss=0.0
        loss+=self._step(anchor,positive,1.0,learning_rate*weight)
        for neg in negative_tokens:
            if neg in self.embeddings: loss+=self._step(anchor,neg,0.0,learning_rate*weight/max(1,len(negative_tokens)))
        return loss
    def _step(self,a:str,b:str,label:float,lr:float)->float:
        va=self.embeddings[a];vb=self.embeddings[b]
        score=dot(va,vb);p=sigmoid(score);g=(p-label)
        old_a=va[:]
        for i in range(self.dimension):
            va[i]-=lr*g*vb[i]
            vb[i]-=lr*g*old_a[i]
        eps=1e-12
        return -(label*math.log(max(eps,p))+(1-label)*math.log(max(eps,1-p)))
    def state_dict(self)->dict:
        return {t:[float(format(x,'.10g')) for x in self.embeddings[t]] for t in sorted(self.embeddings)}
    def state_hash(self)->str:
        return content_hash({"dimension":self.dimension,"seed":self.seed,"embeddings":self.state_dict()})

def checkpoint_payload(encoder:ReferenceEmbeddingEncoder,metadata:dict)->dict:
    payload={"phase":"SAED_V4_11","checkpoint_format":"json_embedding_table_v1","model_family":"deterministic_reference_sgns","dimension":encoder.dimension,"seed":encoder.seed,"vocabulary":list(encoder.vocabulary),"embeddings":encoder.state_dict(),"metadata":metadata,"runtime_authority":False,"selection_authority":False,"execution_authority":False,"synthetic_reference_only":True}
    payload['checkpoint_id']=stable_id('encoderckpt',payload);payload['checkpoint_hash']=content_hash(payload);return payload

def encoder_from_checkpoint(checkpoint:dict)->ReferenceEmbeddingEncoder:
    expected=checkpoint.get('checkpoint_hash');payload={k:v for k,v in checkpoint.items() if k!='checkpoint_hash'}
    if expected!=content_hash(payload): raise CheckpointError('checkpoint hash mismatch')
    return ReferenceEmbeddingEncoder(checkpoint['vocabulary'],checkpoint['dimension'],checkpoint['seed'],checkpoint['embeddings'])
