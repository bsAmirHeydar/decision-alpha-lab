from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any

SAFE_NAME=re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")

def canonical_bytes(obj:Any)->bytes:
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def digest_object(obj:Any)->str:
    return "sha256:"+hashlib.sha256(canonical_bytes(obj)).hexdigest()
def digest_bytes(data:bytes)->str:
    return "sha256:"+hashlib.sha256(data).hexdigest()
def digest_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return "sha256:"+h.hexdigest()
def stable_id(prefix:str,*parts:str)->str:
    raw="|".join(parts).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(raw).hexdigest()[:20].upper()}"
def safe_component(value:str,label:str)->str:
    if not isinstance(value,str) or not SAFE_NAME.fullmatch(value): raise ValueError(f"invalid {label}: {value!r}")
    return value
