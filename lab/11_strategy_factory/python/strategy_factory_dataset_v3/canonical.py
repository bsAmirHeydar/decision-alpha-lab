from __future__ import annotations
import hashlib, json, math, re
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from enum import Enum
from typing import Any
from .errors import ContractError

_SAFE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@/-]{0,255}$")

def safe_id(value:str, field:str="id") -> str:
    if not isinstance(value,str) or not _SAFE.fullmatch(value):
        raise ContractError("unsafe_identifier",f"{field} is not a canonical safe identifier",{"value":str(value)})
    return value

def decimal_text(value:Decimal|int|float|str|None, scale:int=12) -> str|None:
    if value is None: return None
    d=value if isinstance(value,Decimal) else Decimal(str(value))
    if not d.is_finite(): raise ContractError("non_finite_number","NaN and infinity are forbidden")
    q=Decimal(1).scaleb(-scale)
    s=format(d.quantize(q),'f').rstrip('0').rstrip('.')
    return s if s not in ('','-0') else '0'

def canonical_value(value:Any) -> Any:
    if is_dataclass(value): return canonical_value(asdict(value))
    if isinstance(value,Enum): return value.value
    if isinstance(value,Decimal): return decimal_text(value)
    if isinstance(value,float):
        if not math.isfinite(value): raise ContractError("non_finite_number","NaN and infinity are forbidden")
        return decimal_text(value)
    if isinstance(value,dict): return {str(k):canonical_value(value[k]) for k in sorted(value,key=lambda x:str(x))}
    if isinstance(value,(tuple,list)): return [canonical_value(x) for x in value]
    if isinstance(value,(str,int,bool)) or value is None: return value
    raise ContractError("unsupported_canonical_type",f"unsupported canonical type {type(value).__name__}")

def canonical_json(value:Any) -> str:
    return json.dumps(canonical_value(value),sort_keys=True,separators=(',',':'),ensure_ascii=False)

def sha256(value:Any) -> str:
    return hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()

def stable_id(prefix:str, value:Any) -> str:
    safe_id(prefix,'prefix')
    return f"{prefix}_{sha256(value)[:24]}"
