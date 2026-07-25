from __future__ import annotations
from dataclasses import asdict,is_dataclass
from enum import Enum
from hashlib import sha256
import json,re
from .errors import FPI11Error
ID_RE=re.compile(r'^[A-Za-z0-9_.:@/+-]+$')
def primitive(v):
    if is_dataclass(v): return {k:primitive(x) for k,x in asdict(v).items()}
    if isinstance(v,Enum): return v.value
    if isinstance(v,dict): return {str(k):primitive(v[k]) for k in sorted(v)}
    if isinstance(v,(tuple,list)): return [primitive(x) for x in v]
    return v
def canonical_json(v): return json.dumps(primitive(v),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def canonical_sha256(v): return sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix,v): return f'{prefix}-{canonical_sha256(v)[:24]}'
def require_id(v,name='id'):
    if not isinstance(v,str) or not v or not ID_RE.match(v): raise FPI11Error('FP_VIS_ID_INVALID',f'{name} invalid')
    return v
def require_hash(v,name='hash'):
    if not isinstance(v,str) or len(v)!=64 or any(c not in '0123456789abcdef' for c in v): raise FPI11Error('FP_VIS_HASH_INVALID',f'{name} invalid')
    return v
def sorted_unique(v): return tuple(sorted(set(v)))
