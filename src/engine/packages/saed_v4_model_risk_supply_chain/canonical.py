from __future__ import annotations
import hashlib,json
from copy import deepcopy
from typing import Any

def canonical_bytes(value:Any)->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
def content_hash(value:Any)->str:return hashlib.sha256(canonical_bytes(value)).hexdigest()
def stable_id(prefix:str,value:Any,length:int=24)->str:return f"{prefix}_{content_hash(value)[:length]}"
def seal(value:dict,prefix:str,id_field:str,hash_field:str)->dict:
    body=deepcopy(value); body[id_field]=stable_id(prefix,body); body[hash_field]=content_hash(body); return body
def hash_chain(records:list[dict],prefix:str)->list[dict]:
    out=[]; previous="0"*64
    for ordinal,record in enumerate(records):
        x=deepcopy(record); x["ordinal"]=ordinal; x["previous_hash"]=previous; x["event_id"]=stable_id(prefix,x); x["event_hash"]=content_hash(x); previous=x["event_hash"]; out.append(x)
    return out
