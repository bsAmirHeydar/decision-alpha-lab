from __future__ import annotations
from dataclasses import asdict,is_dataclass
from enum import Enum
import hashlib,json,re
from .errors import FPI09Error

def _norm(v):
    if is_dataclass(v): return _norm(asdict(v))
    if isinstance(v,Enum): return v.value
    if isinstance(v,dict): return {str(k):_norm(v[k]) for k in sorted(v,key=lambda x:str(x))}
    if isinstance(v,(tuple,list,set,frozenset)): return [_norm(x) for x in v]
    return v

def canonical_json(v): return json.dumps(_norm(v),sort_keys=True,separators=(",",":"),ensure_ascii=False)
def canonical_sha256(v): return hashlib.sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix,v,length=32): return f"{prefix}_{canonical_sha256(v)[:length]}"
def require_identifier(v,n):
    if not isinstance(v,str) or not re.fullmatch(r"[A-Za-z0-9_.:-]+",v): raise FPI09Error("FP_LDG_IDENTIFIER_INVALID",f"{n} invalid")
    return v
def require_sha256(v,n):
    if not isinstance(v,str) or not re.fullmatch(r"[0-9a-f]{64}",v): raise FPI09Error("FP_LDG_SHA256_INVALID",f"{n} must be lowercase sha256")
    return v
def require_semver(v,n):
    if not isinstance(v,str) or not re.fullmatch(r"\d+\.\d+\.\d+",v): raise FPI09Error("FP_LDG_SEMVER_INVALID",f"{n} invalid")
    return v
