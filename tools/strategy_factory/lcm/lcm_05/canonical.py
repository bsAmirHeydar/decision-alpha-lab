from __future__ import annotations
import hashlib,json,re
from pathlib import PurePosixPath

def canonical_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def sha256_bytes(data:bytes)->str: return "sha256:"+hashlib.sha256(data).hexdigest()
def digest_object(value,omit_key=None):
    if omit_key and isinstance(value,dict): value={k:v for k,v in value.items() if k!=omit_key}
    return sha256_bytes(canonical_bytes(value))
def content_id(prefix,value,length=32): return prefix+"_"+hashlib.sha256(canonical_bytes(value)).hexdigest()[:length].upper()
def slug(value,max_len=56):
    s=re.sub(r"[^A-Za-z0-9]+","_",str(value)).strip("_").upper() or "UNNAMED"
    return s[:max_len]
def posix(path): return PurePosixPath(str(path).replace("\\","/")).as_posix()
