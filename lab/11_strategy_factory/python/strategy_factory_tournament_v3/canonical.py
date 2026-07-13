from __future__ import annotations
import dataclasses,enum,hashlib,json,math
from typing import Any

def normalize(value:Any)->Any:
    if dataclasses.is_dataclass(value): value=dataclasses.asdict(value)
    if isinstance(value,enum.Enum): return value.value
    if isinstance(value,dict): return {str(k):normalize(value[k]) for k in sorted(value,key=lambda x:str(x))}
    if isinstance(value,(list,tuple)): return [normalize(v) for v in value]
    if isinstance(value,set): return [normalize(v) for v in sorted(value,key=repr)]
    if isinstance(value,float):
        if not math.isfinite(value): raise ValueError('non-finite values are not canonical')
        return 0.0 if value==0.0 else float(format(value,'.17g'))
    return value

def canonical_json(value:Any)->str:
    return json.dumps(normalize(value),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def canonical_bytes(value:Any)->bytes:return canonical_json(value).encode('utf-8')
def canonical_sha256(value:Any)->str:return hashlib.sha256(canonical_bytes(value)).hexdigest()
def stable_id(prefix:str,value:Any)->str:return f"{prefix}:{canonical_sha256(value)[:24]}"
