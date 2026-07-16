from __future__ import annotations
import hashlib,json,math

def _normalize(value):
    if isinstance(value,dict): return {str(k):_normalize(value[k]) for k in sorted(value)}
    if isinstance(value,(list,tuple)): return [_normalize(x) for x in value]
    if isinstance(value,float):
        if not math.isfinite(value): raise ValueError('non-finite float')
        return float(format(value,'.15g'))
    return value

def canonical_bytes(value): return json.dumps(_normalize(value),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def content_hash(value): return hashlib.sha256(canonical_bytes(value)).hexdigest()
def stable_id(prefix,value,n=24): return f"{prefix}_{content_hash(value)[:n]}"
def hash_unit(key): return int(hashlib.sha256(str(key).encode('utf-8')).hexdigest()[:16],16)/(16**16-1)
def hash_signed(key): return 2.0*hash_unit(key)-1.0
def artifact_hash(value,field='artifact_hash'):
    return content_hash({k:v for k,v in value.items() if k!=field})
def seal(value,field='artifact_hash'):
    out=dict(value);out[field]=artifact_hash(out,field);return out
