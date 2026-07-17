from __future__ import annotations
import hashlib,json,re
from copy import deepcopy
from typing import Any

def canonical_bytes(value:Any)->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
def content_hash(value:Any)->str:return hashlib.sha256(canonical_bytes(value)).hexdigest()
def stable_id(prefix:str,value:Any,length:int=24)->str:return f"{prefix}_{content_hash(value)[:length]}"
def normalize_text(value:str)->str:
    return " ".join(re.sub(r"[^a-z0-9_\- ]+"," ",value.lower()).split())
def semantic_fingerprint(*parts:Any)->str:
    normalized=[]
    for p in parts:
        if isinstance(p,str): normalized.append(normalize_text(p))
        elif isinstance(p,list): normalized.append(sorted(normalize_text(str(x)) for x in p))
        else: normalized.append(p)
    return content_hash(normalized)
def seal(value:dict,prefix:str,id_field:str,hash_field:str)->dict:
    body=deepcopy(value); body[id_field]=stable_id(prefix,body); body[hash_field]=content_hash(body); return body
def hash_chain(records:list[dict],prefix:str)->list[dict]:
    out=[]; previous="0"*64
    for ordinal,record in enumerate(records):
        x=deepcopy(record); x["ordinal"]=ordinal; x["previous_hash"]=previous; x["event_id"]=stable_id(prefix,x); x["event_hash"]=content_hash(x); previous=x["event_hash"]; out.append(x)
    return out
def merkle_root(hashes:list[str])->str:
    level=sorted(hashes) or ["0"*64]
    while len(level)>1:
        if len(level)%2: level.append(level[-1])
        level=[hashlib.sha256((level[i]+level[i+1]).encode()).hexdigest() for i in range(0,len(level),2)]
    return level[0]
