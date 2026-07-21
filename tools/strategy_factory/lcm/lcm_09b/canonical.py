from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any,Iterable

def canonical_bytes(value:Any, omit:Iterable[str]=())->bytes:
    if isinstance(value,dict): value={k:v for k,v in value.items() if k not in set(omit)}
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def digest_object(value:Any,*omit:str)->str:return "sha256:"+hashlib.sha256(canonical_bytes(value,omit)).hexdigest()
def file_digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return "sha256:"+h.hexdigest()
def stable_id(prefix:str,*parts:object,length:int=32)->str:
    h=hashlib.sha256("".join(str(x) for x in parts).encode("utf-8")).hexdigest()[:length].upper()
    return f"{prefix}_{h}"
