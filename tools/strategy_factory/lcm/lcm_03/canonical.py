from __future__ import annotations
import hashlib, json, re
from pathlib import Path, PurePosixPath
from typing import Any
from .errors import ContractViolation

def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False).encode("utf-8")
def sha256_bytes(data: bytes) -> str: return "sha256:" + hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block=f.read(1024*1024)
            if not block: break
            h.update(block)
    return "sha256:"+h.hexdigest()
def digest_object(value: Any, digest_field: str|None=None) -> str:
    if digest_field and isinstance(value,dict): value={k:v for k,v in value.items() if k!=digest_field}
    return sha256_bytes(canonical_json_bytes(value))
def content_id(prefix: str, material: Any, length: int=32) -> str:
    return f"{prefix}_{hashlib.sha256(canonical_json_bytes(material)).hexdigest()[:length].upper()}"
def normalize_root_relative(raw: str) -> str:
    if not isinstance(raw,str) or not raw.strip(): raise ContractViolation("path must be non-empty")
    p=PurePosixPath(raw.replace('\\','/'))
    if p.is_absolute() or any(part in {'','.','..'} for part in p.parts): raise ContractViolation(f"unsafe path: {raw}")
    return p.as_posix()
def normalize_token(raw: str, max_len: int=48) -> str:
    value=re.sub(r'[^A-Z0-9]+','_',raw.upper()).strip('_')
    value=re.sub(r'_+','_',value)
    return (value or 'UNNAMED')[:max_len]
def normalize_alias(raw: str, case_sensitive: bool=False) -> str:
    value=raw.replace('\\','/').strip()
    return value if case_sensitive else value.casefold()
