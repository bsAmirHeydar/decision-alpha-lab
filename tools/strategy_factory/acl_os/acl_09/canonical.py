from __future__ import annotations
import hashlib,json,math,re
from pathlib import Path
from typing import Any
DIGEST_RE=re.compile(r"^sha256:[0-9a-f]{64}$")
def _norm(v:Any)->Any:
    if isinstance(v,dict): return {str(k):_norm(x) for k,x in sorted(v.items(),key=lambda z:str(z[0]))}
    if isinstance(v,(list,tuple,set)): return [_norm(x) for x in v]
    if isinstance(v,float):
        if not math.isfinite(v): raise ValueError('ACL09_NON_FINITE_NUMBER')
        return int(v) if v.is_integer() else float(format(v,'.15g'))
    return v
def canonical_bytes(v:Any)->bytes: return json.dumps(_norm(v),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def digest_object(v:Any)->str: return 'sha256:'+hashlib.sha256(canonical_bytes(v)).hexdigest()
def digest_bytes(v:bytes)->str: return 'sha256:'+hashlib.sha256(v).hexdigest()
def digest_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return 'sha256:'+h.hexdigest()
def stable_id(prefix:str,*parts:str,length:int=24)->str: return f"{prefix}_{hashlib.sha256('|'.join(parts).encode()).hexdigest()[:length].upper()}"
def with_digest(body:dict[str,Any],field:str)->dict[str,Any]: return {**body,field:digest_object(body)}
def verify_embedded_digest(doc:dict[str,Any],field:str)->bool:
    return isinstance(doc.get(field),str) and DIGEST_RE.fullmatch(doc[field]) is not None and doc[field]==digest_object({k:v for k,v in doc.items() if k!=field})
