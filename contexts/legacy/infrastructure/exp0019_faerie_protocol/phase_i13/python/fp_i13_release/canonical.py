from __future__ import annotations
from dataclasses import asdict,is_dataclass
from enum import Enum
import hashlib,json,re
from .errors import FPI13Error
_ID=re.compile(r'^[A-Za-z0-9_.:@+/\\-]{1,256}$')
def primitive(v):
    if is_dataclass(v): return {k:primitive(x) for k,x in asdict(v).items()}
    if isinstance(v,Enum): return v.value
    if isinstance(v,dict): return {str(k):primitive(v[k]) for k in sorted(v)}
    if isinstance(v,(tuple,list)): return [primitive(x) for x in v]
    if isinstance(v,(set,frozenset)): return [primitive(x) for x in sorted(v,key=str)]
    return v
def canonical_json(v): return json.dumps(primitive(v),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def sha256(v): return hashlib.sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix,v,length=24): return f'{prefix}-{sha256(v)[:length]}'
def require_id(v,name):
    if not isinstance(v,str) or not _ID.fullmatch(v): raise FPI13Error('FP_REL_ID_INVALID',f'{name} invalid')
    return v
def require_hash(v,name):
    if not isinstance(v,str) or not re.fullmatch(r'[0-9a-f]{64}',v): raise FPI13Error('FP_REL_HASH_INVALID',f'{name} invalid')
    return v
def sorted_unique(values): return tuple(sorted(set(values)))
