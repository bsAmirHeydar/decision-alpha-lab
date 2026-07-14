from __future__ import annotations
from dataclasses import asdict,is_dataclass
from enum import Enum
import hashlib,json,re
from .errors import FPI12Error
_ID=re.compile(r'^[A-Za-z0-9_.:@+\-/]{1,256}$')
def primitive(v):
    if is_dataclass(v): return {k:primitive(x) for k,x in asdict(v).items()}
    if isinstance(v,Enum): return v.value
    if isinstance(v,dict): return {str(k):primitive(v[k]) for k in sorted(v)}
    if isinstance(v,(tuple,list,set,frozenset)): return [primitive(x) for x in (sorted(v,key=str) if isinstance(v,(set,frozenset)) else v)]
    return v
def canonical_json(v): return json.dumps(primitive(v),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def sha256(v): return hashlib.sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix,v): return f'{prefix}-{sha256(v)[:24]}'
def require_id(v,name):
    if not isinstance(v,str) or not _ID.fullmatch(v): raise FPI12Error('FP_UX_ID_INVALID',f'{name} invalid')
    return v
def require_hash(v,name):
    if not isinstance(v,str) or not re.fullmatch(r'[0-9a-f]{64}',v): raise FPI12Error('FP_UX_HASH_INVALID',f'{name} invalid')
    return v
def sorted_unique(values): return tuple(sorted(set(values)))
