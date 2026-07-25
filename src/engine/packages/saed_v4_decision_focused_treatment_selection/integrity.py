from __future__ import annotations
from .canonical import content_hash
from .errors import IntegrityError

def verify_upstream_hashes(upstream,expected):
    for key,value in expected.items():
        if key not in upstream or upstream[key]!=value:raise IntegrityError(f'upstream hash mismatch: {key}')
    return True
def seal_registry(rows):
    out={'rows':sorted(rows,key=lambda x:tuple(str(x.get(k,'')) for k in sorted(x))),'immutable':True};out['registry_hash']=content_hash(out);return out
