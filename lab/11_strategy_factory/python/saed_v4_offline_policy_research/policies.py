from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import normalize

def make_policy(family,states,metadata=None):
    normalized={}
    for state,dist in sorted(states.items()):
        keys=sorted(dist);vals=normalize([dist[k] for k in keys]);normalized[state]={k:vals[i] for i,k in enumerate(keys)}
    core={'family':str(family),'states':normalized,'metadata':metadata or {},'research_only':True,'runtime_executable':False,'promotion_eligible':False}
    core['policy_id']=stable_id(f'{family}_policy',core);core['policy_hash']=content_hash(core);return core

def baseline_from_document(doc): return make_policy('manual_baseline',doc['states'],{'source':doc['policy_id'],'immutable':True})
