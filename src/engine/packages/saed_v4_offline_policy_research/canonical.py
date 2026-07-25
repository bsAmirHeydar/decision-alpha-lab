from __future__ import annotations
import hashlib,json,math

def _norm(v):
    if isinstance(v,dict): return {str(k):_norm(v[k]) for k in sorted(v)}
    if isinstance(v,(list,tuple)): return [_norm(x) for x in v]
    if isinstance(v,float):
        if not math.isfinite(v): raise ValueError('non-finite float')
        return float(format(v,'.15g'))
    return v

def canonical_bytes(v): return json.dumps(_norm(v),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def content_hash(v): return hashlib.sha256(canonical_bytes(v)).hexdigest()
def stable_id(prefix,v,n=24): return f'{prefix}_{content_hash(v)[:n]}'
def artifact_hash(v,field='artifact_hash'): return content_hash({k:x for k,x in v.items() if k!=field})
def seal(v,field='artifact_hash'):
    o=dict(v);o[field]=artifact_hash(o,field);return o
