from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any
def canonical_bytes(value:Any)->bytes:return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
def digest_object(value:Any,omit:str|None=None)->str:
    if omit and isinstance(value,dict): value={k:v for k,v in value.items() if k!=omit}
    return "sha256:"+hashlib.sha256(canonical_bytes(value)).hexdigest()
def file_digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return "sha256:"+h.hexdigest()
