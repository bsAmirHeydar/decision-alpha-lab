from __future__ import annotations
import hashlib, math

def cfloat(value: float) -> str:
    if not math.isfinite(value):
        raise ValueError("non-finite canonical float")
    return format(value, ".12f")

def cbool(value: bool) -> str:
    return "1" if value else "0"

def stable_id(prefix: str, canonical: str) -> str:
    return f"{prefix}_{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:32]}"

def chain_hash(previous_hash: str, canonical: str) -> str:
    return hashlib.sha256((previous_hash + "|" + canonical).encode("utf-8")).hexdigest()
