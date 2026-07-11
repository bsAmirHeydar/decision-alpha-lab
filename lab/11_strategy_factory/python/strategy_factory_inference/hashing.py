from __future__ import annotations
import hashlib, math

def stable_id(prefix: str, *parts: object) -> str:
    return prefix + "_" + hashlib.sha256("|".join(str(x) for x in parts).encode()).hexdigest()[:16]

def sha256_bytes(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def sha256_lines(lines) -> str: return hashlib.sha256(("\n".join(lines)+"\n").encode()).hexdigest()
def cfloat(v: float) -> str:
    if not math.isfinite(v): raise ValueError("non-finite canonical float")
    return format(v, ".17g")
def cbool(v: bool) -> str: return "1" if v else "0"
def fnv1a64(data: bytes) -> str:
    h=0xcbf29ce484222325
    for b in data:
        h ^= b; h=(h*0x100000001b3)&0xffffffffffffffff
    return f"{h:016x}"
