from __future__ import annotations
import hashlib,json,math
from typing import Any

def normalise(v:Any)->Any:
    if isinstance(v,dict): return {str(k):normalise(v[k]) for k in sorted(v)}
    if isinstance(v,(list,tuple)): return [normalise(x) for x in v]
    if isinstance(v,float):
        if not math.isfinite(v): raise ValueError('non-finite float')
        return 0.0 if v==0.0 else float(format(v,'.12g'))
    return v

def canonical_json(v:Any)->str: return json.dumps(normalise(v),sort_keys=True,separators=(',',':'),ensure_ascii=False)
def content_hash(v:Any)->str: return hashlib.sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix:str,v:Any)->str: return f"{prefix}_{content_hash(v)[:24]}"
def hash_unit(seed:str)->float: return int(hashlib.sha256(seed.encode()).hexdigest()[:16],16)/float(0xffffffffffffffff)
def hash_signed(seed:str)->float: return hash_unit(seed)*2.0-1.0

def merkle_root(hashes:list[str])->str:
    if not hashes:return hashlib.sha256(b'').hexdigest()
    layer=[bytes.fromhex(h) for h in hashes]
    while len(layer)>1:
        if len(layer)%2:layer.append(layer[-1])
        layer=[hashlib.sha256(layer[i]+layer[i+1]).digest() for i in range(0,len(layer),2)]
    return layer[0].hex()
