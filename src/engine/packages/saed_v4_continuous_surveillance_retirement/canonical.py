from __future__ import annotations
import hashlib,json
from copy import deepcopy
from decimal import Decimal,ROUND_HALF_EVEN
from typing import Any
Q=Decimal("0.00000001")
def q(v:Any)->float:return float(Decimal(str(v)).quantize(Q,rounding=ROUND_HALF_EVEN))
def canonical_bytes(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
def content_hash(v:Any)->str:return hashlib.sha256(canonical_bytes(v)).hexdigest()
def stable_id(prefix:str,v:Any,length:int=24)->str:return f"{prefix}_{content_hash(v)[:length]}"
def seal(v:dict,prefix:str,id_field:str,hash_field:str)->dict:
 x=deepcopy(v);x[id_field]=stable_id(prefix,x);x[hash_field]=content_hash(x);return x
def hash_chain(records:list[dict],prefix:str)->list[dict]:
 out=[];prev="0"*64
 for ordinal,r in enumerate(records):
  x=deepcopy(r);x["ordinal"]=ordinal;x["previous_hash"]=prev;x["event_id"]=stable_id(prefix,x);x["event_hash"]=content_hash(x);prev=x["event_hash"];out.append(x)
 return out
def merkle_root(hashes:list[str])->str:
 level=sorted(hashes) or ["0"*64]
 while len(level)>1:
  if len(level)%2:level.append(level[-1])
  level=[hashlib.sha256((level[i]+level[i+1]).encode()).hexdigest() for i in range(0,len(level),2)]
 return level[0]
