from __future__ import annotations
from .canonical import content_hash, stable_id, hash_unit
from .models import TokenStream
from .errors import ContractError

def sample_token_negatives(vocabulary:list[str], positive:str, count:int, seed_key:str)->list[str]:
    candidates=[t for t in vocabulary if t!=positive and not t.startswith('[')]
    if len(candidates)<count: raise ContractError('insufficient negative vocabulary')
    ranked=sorted(candidates,key=lambda t:(hash_unit(seed_key+'|'+t),t))
    return ranked[:count]

def sample_temporal_negative(anchor:TokenStream, streams:list[TokenStream], seed_key:str)->TokenStream:
    candidates=[s for s in streams if s.split=='train' and s.root_context_id!=anchor.root_context_id and s.known_time<=anchor.known_time]
    if not candidates:
        candidates=[s for s in streams if s.split=='train' and s.root_context_id!=anchor.root_context_id]
    if not candidates: raise ContractError('no dependency-safe temporal negative')
    return sorted(candidates,key=lambda s:(hash_unit(seed_key+'|'+s.record_id),s.record_id))[0]

def build_negative_plan(streams:list[TokenStream], vocabulary:list[str], count:int, seed:int)->dict:
    items=[]
    for s in streams:
        if s.split!='train': continue
        candidates=[t for t in s.tokens if not t.startswith('[')]
        if not candidates: continue
        positive=sorted(candidates)[0]
        negative_tokens=sample_token_negatives(vocabulary,positive,count,f'{seed}|{s.record_id}|token')
        temporal=sample_temporal_negative(s,streams,f'{seed}|{s.record_id}|temporal')
        items.append({"record_id":s.record_id,"positive_token":positive,"negative_tokens":negative_tokens,"temporal_negative_record_id":temporal.record_id,"anchor_known_time":s.known_time,"negative_known_time":temporal.known_time,"different_root":temporal.root_context_id!=s.root_context_id})
    payload={"phase":"SAED_V4_11","seed":seed,"negative_count":count,"items":items,"dependency_safe":all(x['different_root'] for x in items)}
    payload['plan_id']=stable_id('negativeplan',payload);payload['plan_hash']=content_hash(payload)
    return payload
