from __future__ import annotations
import math
from typing import Any
from .canonical import content_hash, stable_id
from .models import CorpusRecord, TokenStream
from .errors import ContractError, LeakageError
from .validation import scan_forbidden

SPECIAL_TOKENS=("[PAD]","[MASK]","[UNK]","[RECORD]","[VIEW]","[GRAPH]","[DESC]")

def _scalar_token(view:str,key:str,value:Any)->str:
    if value is None: val='NULL'
    elif isinstance(value,bool): val='TRUE' if value else 'FALSE'
    elif isinstance(value,(int,float)):
        if isinstance(value,float) and not math.isfinite(value): raise ContractError('non-finite feature')
        val=f'{float(value):.6g}'
    elif isinstance(value,(list,tuple)): val='|'.join(str(x) for x in value[:16])
    else: val=str(value)
    token=f'VIEW::{view}::{key}::{val}'
    scan_forbidden(token)
    return token

def tokenize_record(record:CorpusRecord, split:str)->TokenStream:
    tokens=['[RECORD]']
    masks={}
    for view in sorted(record.views):
        features=record.views[view]
        present=bool(features)
        masks[view]=0 if present else 1
        tokens.extend(['[VIEW]',f'VIEW_KIND::{view}',f'VIEW_MASK::{view}::{"PRESENT" if present else "MISSING"}'])
        for key in sorted(features): tokens.append(_scalar_token(view,key,features[key]))
    tokens.append('[GRAPH]')
    for relation in sorted(record.graph_relations):
        token=f'GRAPH_REL::{relation}';scan_forbidden(token);tokens.append(token)
    tokens.append('[DESC]')
    for descriptor in sorted(record.descriptor_tokens):
        token=f'DESC::{descriptor}';scan_forbidden(token);tokens.append(token)
    tokens.extend([f'DOMAIN::{record.domain_id}',f'ROLE::{record.evidence_role}',f'SYNTHETIC::{str(record.synthetic).upper()}'])
    token_tuple=tuple(tokens)
    return TokenStream(record.record_id,record.context_id,record.root_context_id,record.domain_id,record.event_time,record.known_time,split,token_tuple,masks,content_hash(list(token_tuple)))

def build_token_streams(records:list[CorpusRecord], split_manifest:dict)->list[TokenStream]:
    lookup={x['record_id']:x['split'] for x in split_manifest['assignments']}
    streams=[]
    for record in sorted(records,key=lambda x:(x.known_time,x.record_id)):
        if record.record_id not in lookup: raise ContractError('record missing split assignment')
        streams.append(tokenize_record(record,lookup[record.record_id]))
    return streams

def build_tokenizer_spec(streams:list[TokenStream])->dict:
    vocab=sorted(set(SPECIAL_TOKENS)|{t for s in streams for t in s.tokens})
    token_to_id={t:i for i,t in enumerate(vocab)}
    payload={"phase":"SAED_V4_11","exact_version":"1.0.0","normalization":"canonical_scalar_v1","special_tokens":list(SPECIAL_TOKENS),"vocabulary":vocab,"token_to_id":token_to_id,"vocabulary_size":len(vocab),"unknown_policy":"fail_closed_to_[UNK]","future_suffix_allowed":False,"outcome_tokens_allowed":False}
    payload['tokenizer_id']=stable_id('tokenizer',payload);payload['tokenizer_hash']=content_hash(payload)
    return payload

def stream_to_dict(s:TokenStream)->dict:
    return {"record_id":s.record_id,"context_id":s.context_id,"root_context_id":s.root_context_id,"domain_id":s.domain_id,"event_time":s.event_time,"known_time":s.known_time,"split":s.split,"tokens":list(s.tokens),"view_masks":dict(s.view_masks),"token_hash":s.token_hash}
