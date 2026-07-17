from __future__ import annotations
import hashlib, json, math, re
from pathlib import Path
from typing import Any

DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SAFE_ID_RE = re.compile(r"^[A-Z][A-Z0-9_.:-]{2,127}$")

def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in sorted(value.items(), key=lambda x: str(x[0]))}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("ACL05_NON_FINITE_NUMBER")
        return int(value) if value.is_integer() else float(format(value, ".15g"))
    return value

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest_object(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()

def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()

def digest_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return "sha256:"+h.hexdigest()

def stable_id(prefix: str, *parts: str, length: int=24) -> str:
    raw="|".join(parts).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(raw).hexdigest()[:length].upper()}"

def with_digest(body: dict[str, Any], field: str) -> dict[str, Any]:
    return {**body, field: digest_object(body)}

def verify_embedded_digest(document: dict[str, Any], field: str) -> bool:
    supplied=document.get(field)
    return bool(isinstance(supplied,str) and DIGEST_RE.fullmatch(supplied) and supplied==digest_object({k:v for k,v in document.items() if k!=field}))
