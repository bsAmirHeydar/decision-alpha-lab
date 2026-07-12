from __future__ import annotations
import hashlib, json, re
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Mapping, Sequence
from .errors import TreatmentError
_SAFE=re.compile(r'^[A-Za-z0-9._:/-]{1,160}$')
def safe_id(v:str,field:str)->str:
    if not isinstance(v,str) or not _SAFE.fullmatch(v): raise TreatmentError('unsafe_identifier',f'{field} is unsafe',{'value':str(v)})
    return v
def dec(v:Any)->Decimal:
    try: return Decimal(str(v))
    except Exception as e: raise TreatmentError('invalid_decimal','value cannot be converted to Decimal',{'value':str(v)}) from e
def q(v:Any,scale:int=10)->str:
    x=dec(v).quantize(Decimal(1).scaleb(-scale),rounding=ROUND_HALF_UP)
    s=format(x,'f').rstrip('0').rstrip('.')
    return s if s and s!='-0' else '0'
def canonical_value(v:Any)->Any:
    if isinstance(v,Decimal): return q(v)
    if isinstance(v,float): return q(v)
    if isinstance(v,Mapping): return {str(k):canonical_value(v[k]) for k in sorted(v)}
    if isinstance(v,Sequence) and not isinstance(v,(str,bytes,bytearray)): return [canonical_value(x) for x in v]
    if hasattr(v,'value'): return v.value
    if hasattr(v,'to_dict'): return canonical_value(v.to_dict())
    return v
def canonical_json(v:Any)->str: return json.dumps(canonical_value(v),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def digest(v:Any,n:int=24)->str: return hashlib.sha256(canonical_json(v).encode()).hexdigest()[:n]
def stable_id(prefix:str,v:Any)->str: return f'{prefix}_{digest(v)}'
def require(cond:bool,code:str,message:str,details:dict|None=None):
    if not cond: raise TreatmentError(code,message,details)
