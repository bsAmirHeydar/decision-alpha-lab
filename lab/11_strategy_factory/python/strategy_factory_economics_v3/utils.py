from __future__ import annotations
from decimal import Decimal,ROUND_FLOOR,ROUND_CEILING,ROUND_HALF_UP
from typing import Any,Mapping,Sequence
import hashlib,json,re
_SAFE=re.compile(r'^[A-Za-z0-9._:/@-]{1,192}$')
def dec(v:Any)->Decimal: return v if isinstance(v,Decimal) else Decimal(str(v))
def q(v:Any,scale:int=10)->str:
    x=dec(v).quantize(Decimal(1).scaleb(-scale),rounding=ROUND_HALF_UP); s=format(x,'f').rstrip('0').rstrip('.')
    return s if s and s!='-0' else '0'
def canonical_value(v:Any)->Any:
    if isinstance(v,Decimal) or isinstance(v,float): return q(v)
    if isinstance(v,Mapping): return {str(k):canonical_value(v[k]) for k in sorted(v)}
    if isinstance(v,Sequence) and not isinstance(v,(str,bytes,bytearray)): return [canonical_value(x) for x in v]
    if hasattr(v,'value'): return v.value
    if hasattr(v,'to_dict'): return canonical_value(v.to_dict())
    return v
def canonical_json(v:Any)->str: return json.dumps(canonical_value(v),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def stable_id(prefix:str,v:Any,n:int=24)->str: return f'{prefix}_{hashlib.sha256(canonical_json(v).encode()).hexdigest()[:n]}'
def safe_id(v:str,name='identifier')->str:
    if not isinstance(v,str) or not _SAFE.fullmatch(v): raise ValueError(f'unsafe {name}: {v!r}')
    return v
def floor_step(value,step):
    value,step=dec(value),dec(step)
    if step<=0: raise ValueError('step must be positive')
    return (value/step).to_integral_value(rounding=ROUND_FLOOR)*step
def ceil_step(value,step):
    value,step=dec(value),dec(step)
    if step<=0: raise ValueError('step must be positive')
    return (value/step).to_integral_value(rounding=ROUND_CEILING)*step
def round_tick(value,tick,rounding=ROUND_HALF_UP): return (dec(value)/dec(tick)).to_integral_value(rounding=rounding)*dec(tick)
def clamp(v,lo,hi): return max(dec(lo),min(dec(hi),dec(v)))
