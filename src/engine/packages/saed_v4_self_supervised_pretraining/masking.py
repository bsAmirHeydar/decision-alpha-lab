from __future__ import annotations
from .canonical import content_hash, stable_id, hash_unit
from .models import TokenStream
from .errors import ContractError

PROTECTED_PREFIXES=("[","ROLE::","SYNTHETIC::","DOMAIN::","VIEW_KIND::")

def deterministic_mask_positions(stream:TokenStream, seed:int, ratio:float=0.15, max_span:int=3)->list[int]:
    if not 0<ratio<1: raise ContractError('mask ratio outside (0,1)')
    eligible=[i for i,t in enumerate(stream.tokens) if not t.startswith(PROTECTED_PREFIXES)]
    if not eligible: return []
    target=max(1,round(len(eligible)*ratio))
    ranked=sorted(eligible,key=lambda i:(hash_unit(f'{seed}|{stream.record_id}|{i}|{stream.tokens[i]}'),i))
    chosen=set()
    for start in ranked:
        span=1+int(hash_unit(f'span|{seed}|{stream.record_id}|{start}')*max_span)
        for i in range(start,min(len(stream.tokens),start+span)):
            if i in eligible: chosen.add(i)
            if len(chosen)>=target: break
        if len(chosen)>=target: break
    return sorted(chosen)

def apply_mask(stream:TokenStream, positions:list[int])->dict:
    tokens=list(stream.tokens);targets=[]
    for i in positions:
        if not 0<=i<len(tokens): raise ContractError('mask index out of range')
        targets.append({"position":i,"token":tokens[i]});tokens[i]='[MASK]'
    payload={"record_id":stream.record_id,"seeded":True,"positions":positions,"masked_tokens":tokens,"targets":targets,"source_token_hash":stream.token_hash}
    payload['masking_id']=stable_id('masking',payload);payload['masking_hash']=content_hash(payload)
    return payload

def build_masking_plan(streams:list[TokenStream], seed:int, ratio:float=0.15)->dict:
    items=[apply_mask(s,deterministic_mask_positions(s,seed,ratio)) for s in streams if s.split=='train']
    payload={"phase":"SAED_V4_11","seed":seed,"ratio":ratio,"items":items,"record_count":len(items),"future_suffix_allowed":False}
    payload['plan_id']=stable_id('maskplan',payload);payload['plan_hash']=content_hash(payload)
    return payload
