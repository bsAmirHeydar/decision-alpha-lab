from __future__ import annotations
import hashlib,json,random,re
from decimal import Decimal,ROUND_HALF_UP
from typing import Any,Mapping,Sequence
_SAFE=re.compile(r'^[A-Za-z0-9._:/@-]{1,192}$')
def safe_id(value:str,field:str='identifier')->str:
    if not isinstance(value,str) or not _SAFE.fullmatch(value): raise ValueError(f'unsafe {field}: {value!r}')
    return value
def dec(value:Any)->Decimal: return Decimal(str(value))
def q(value:Any,scale:int=10)->str:
    x=dec(value).quantize(Decimal(1).scaleb(-scale),rounding=ROUND_HALF_UP)
    s=format(x,'f').rstrip('0').rstrip('.')
    return s if s and s!='-0' else '0'
def canonical_value(value:Any)->Any:
    if isinstance(value,Decimal): return q(value)
    if isinstance(value,float): return q(value)
    if isinstance(value,Mapping): return {str(k):canonical_value(value[k]) for k in sorted(value)}
    if isinstance(value,Sequence) and not isinstance(value,(str,bytes,bytearray)): return [canonical_value(x) for x in value]
    if hasattr(value,'value'): return value.value
    if hasattr(value,'to_dict'): return canonical_value(value.to_dict())
    return value
def canonical_json(value:Any)->str: return json.dumps(canonical_value(value),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def digest(value:Any,n:int=24)->str: return hashlib.sha256(canonical_json(value).encode()).hexdigest()[:n]
def stable_id(prefix:str,value:Any)->str: return f'{prefix}_{digest(value)}'
def seeded_sample(items:list[Any],count:int,seed:int)->list[Any]:
    r=random.Random(seed); idx=sorted(r.sample(range(len(items)),count)); return [items[i] for i in idx]
