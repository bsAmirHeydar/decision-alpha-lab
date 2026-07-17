from __future__ import annotations
import hashlib,json
from typing import Any

def canonical_json(value:Any)->str:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def content_hash(value:Any)->str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
def bytes_hash(value:bytes)->str:
    return hashlib.sha256(value).hexdigest()
def stable_id(prefix:str,value:Any,length:int=24)->str:
    return f"{prefix}_{content_hash(value)[:length]}"
def without(value:dict,*keys:str)->dict:
    return {k:v for k,v in value.items() if k not in set(keys)}
