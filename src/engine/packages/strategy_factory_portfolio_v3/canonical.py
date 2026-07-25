from __future__ import annotations
import dataclasses, enum, hashlib, json, math
from pathlib import PurePosixPath
from .errors import PortfolioError

def _norm(v):
    if dataclasses.is_dataclass(v): return _norm(dataclasses.asdict(v))
    if isinstance(v,enum.Enum): return v.value
    if isinstance(v,dict): return {str(k):_norm(v[k]) for k in sorted(v)}
    if isinstance(v,(list,tuple)): return [_norm(x) for x in v]
    if isinstance(v,float):
        if not math.isfinite(v): raise PortfolioError('non_finite','non-finite value is forbidden')
        return 0.0 if v==0 else float(format(v,'.12g'))
    return v

def canonical_json(v): return json.dumps(_norm(v),sort_keys=True,separators=(',',':'),ensure_ascii=False)
def canonical_sha256(v): return hashlib.sha256(canonical_json(v).encode()).hexdigest()
def safe_relative_path(v):
    p=PurePosixPath(str(v).replace('\\','/'))
    if p.is_absolute() or '..' in p.parts or not p.parts: raise PortfolioError('unsafe_path','path must be safe and relative',{'path':str(v)})
    return str(p)
