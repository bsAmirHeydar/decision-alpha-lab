from __future__ import annotations
from dataclasses import asdict,is_dataclass
from enum import Enum
import hashlib,json,re
from .errors import FPI07Error

def _norm(v):
    if is_dataclass(v): return _norm(asdict(v))
    if isinstance(v,Enum): return v.value
    if isinstance(v,dict): return {str(k):_norm(v[k]) for k in sorted(v,key=str)}
    if isinstance(v,(tuple,list)): return [_norm(x) for x in v]
    return v

def canonical_json(v): return json.dumps(_norm(v),sort_keys=True,separators=(",",":"),ensure_ascii=False)
def canonical_sha256(v): return hashlib.sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix, material, length=32): return f"{prefix}-{canonical_sha256(material)[:length]}"
def require_identifier(v,name):
    if not isinstance(v,str) or not re.fullmatch(r"[A-Za-z0-9_.:-]+",v): raise FPI07Error("FP_CRC_IDENTIFIER_INVALID",f"{name} invalid",{"field":name})
    return v
def require_sha256(v,name):
    if not isinstance(v,str) or not re.fullmatch(r"[0-9a-f]{64}",v): raise FPI07Error("FP_CRC_SHA256_INVALID",f"{name} must be lowercase sha256")
    return v
def require_semver(v,name):
    if not isinstance(v,str) or not re.fullmatch(r"\d+\.\d+\.\d+",v): raise FPI07Error("FP_CRC_SEMVER_INVALID",f"{name} must be semver")
    return v
