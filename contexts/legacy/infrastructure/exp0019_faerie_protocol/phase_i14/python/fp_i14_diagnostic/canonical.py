from __future__ import annotations
import dataclasses, enum, hashlib, json, re
from .errors import FPI14Error
_HASH=re.compile(r"^[0-9a-f]{64}$")
def primitive(value):
    if dataclasses.is_dataclass(value): return {f.name:primitive(getattr(value,f.name)) for f in dataclasses.fields(value)}
    if isinstance(value,enum.Enum): return value.value
    if isinstance(value,dict): return {str(k):primitive(v) for k,v in sorted(value.items(),key=lambda x:str(x[0]))}
    if isinstance(value,(tuple,list)): return [primitive(v) for v in value]
    if isinstance(value,(set,frozenset)): return sorted(primitive(v) for v in value)
    return value
def canonical_json(value): return json.dumps(primitive(value),sort_keys=True,separators=(",",":"),ensure_ascii=True)
def sha256(value):
    raw=value if isinstance(value,(bytes,bytearray)) else canonical_json(value).encode()
    return hashlib.sha256(raw).hexdigest()
def stable_id(prefix,value,length=24): return f"{prefix}-{sha256(value)[:length]}"
def require_hash(value,name):
    if not isinstance(value,str) or not _HASH.fullmatch(value): raise FPI14Error("FP_DIAG_HASH_INVALID",f"{name} must be lowercase SHA-256")
    return value
def require_id(value,name):
    if not isinstance(value,str) or not value.strip() or len(value)>256: raise FPI14Error("FP_DIAG_ID_INVALID",f"{name} invalid")
    return value
def sorted_unique(values): return tuple(sorted(set(values)))
