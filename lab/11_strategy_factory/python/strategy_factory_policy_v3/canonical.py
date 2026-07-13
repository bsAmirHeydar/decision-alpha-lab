from __future__ import annotations
import dataclasses, enum, hashlib, json, math
from typing import Any
from .errors import PolicyError

def normalize(value:Any)->Any:
    if dataclasses.is_dataclass(value): return normalize(dataclasses.asdict(value))
    if isinstance(value,enum.Enum): return value.value
    if isinstance(value,dict): return {str(k):normalize(value[k]) for k in sorted(value,key=str)}
    if isinstance(value,(list,tuple)): return [normalize(v) for v in value]
    if isinstance(value,float):
        if not math.isfinite(value): raise PolicyError('non_finite_value','canonical payload cannot contain NaN or infinity')
        return 0.0 if value==0 else value
    if isinstance(value,(str,int,bool)) or value is None: return value
    raise PolicyError('unsupported_canonical_type',f'unsupported canonical type: {type(value).__name__}')

def canonical_json(value:Any)->str: return json.dumps(normalize(value),sort_keys=True,separators=(',',':'),ensure_ascii=False)
def canonical_sha256(value:Any)->str: return hashlib.sha256(canonical_json(value).encode()).hexdigest()
def stable_id(prefix:str,value:Any)->str: return f'{prefix}:{canonical_sha256(value)[:24]}'
