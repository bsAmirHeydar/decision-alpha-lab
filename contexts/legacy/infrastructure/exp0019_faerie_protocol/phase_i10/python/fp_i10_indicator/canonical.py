from __future__ import annotations
from dataclasses import asdict,is_dataclass
from enum import Enum
import hashlib,json,re
from .errors import FPI10Error

SHA_RE=re.compile(r"^[0-9a-f]{64}$")
ID_RE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@/\-]{0,255}$")
SEMVER_RE=re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9_.-]+)?$")

def canonicalize(value):
    if is_dataclass(value): value=asdict(value)
    if isinstance(value,Enum): return value.value
    if isinstance(value,dict): return {str(k):canonicalize(value[k]) for k in sorted(value,key=lambda x:str(x))}
    if isinstance(value,(list,tuple)): return [canonicalize(v) for v in value]
    if isinstance(value,set): return sorted(canonicalize(v) for v in value)
    if isinstance(value,float):
        if value == 0.0: return 0.0
        return float(format(value,'.15g'))
    return value

def canonical_json(value): return json.dumps(canonicalize(value),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def canonical_sha256(value): return hashlib.sha256(canonical_json(value).encode()).hexdigest()
def stable_id(prefix,value,length=24): return f"{prefix}_{canonical_sha256(value)[:length]}"

def require_identifier(value,name):
    if not isinstance(value,str) or not ID_RE.fullmatch(value): raise FPI10Error("FP_IND_IDENTIFIER_INVALID",f"{name} invalid")
    return value

def require_sha256(value,name):
    if not isinstance(value,str) or not SHA_RE.fullmatch(value): raise FPI10Error("FP_IND_SHA256_INVALID",f"{name} invalid")
    return value

def require_semver(value,name):
    if not isinstance(value,str) or not SEMVER_RE.fullmatch(value): raise FPI10Error("FP_IND_VERSION_INVALID",f"{name} invalid")
    return value

def require_m1(value,name):
    if not isinstance(value,int) or value<0 or value%60000: raise FPI10Error("FP_IND_M1_TIME_INVALID",f"{name} must be UTC M1 aligned milliseconds")
    return value

def sorted_unique(values): return tuple(sorted(set(values)))
