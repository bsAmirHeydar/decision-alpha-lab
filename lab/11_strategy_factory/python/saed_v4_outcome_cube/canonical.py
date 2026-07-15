from __future__ import annotations
import hashlib,json,math
from decimal import Decimal
from typing import Any,Iterable
from .errors import ContractError

def _normalise(value:Any)->Any:
    if isinstance(value,Decimal): return format(value,'f')
    if isinstance(value,float):
        if not math.isfinite(value): raise ContractError('non-finite number is prohibited')
        return format(Decimal(str(value)).normalize(),'f')
    if isinstance(value,dict): return {str(k):_normalise(value[k]) for k in sorted(value)}
    if isinstance(value,(list,tuple)): return [_normalise(v) for v in value]
    if isinstance(value,set): return sorted(_normalise(v) for v in value)
    return value

def canonical_json(value:Any)->str:
    return json.dumps(_normalise(value),sort_keys=True,separators=(',',':'),ensure_ascii=False)

def content_hash(value:Any)->str:
    return hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()

def stable_id(prefix:str,value:Any,width:int=24)->str:
    return f'{prefix}_{content_hash(value)[:width]}'

def merkle_root(hashes:Iterable[str])->str:
    layer=sorted(str(x) for x in hashes)
    if not layer:return hashlib.sha256(b'').hexdigest()
    while len(layer)>1:
        if len(layer)%2:layer.append(layer[-1])
        layer=[hashlib.sha256((layer[i]+layer[i+1]).encode()).hexdigest() for i in range(0,len(layer),2)]
    return layer[0]
