from __future__ import annotations
import hashlib, math

def fnv1a64_utf16le(text: str) -> int:
    value = 0xCBF29CE484222325
    for byte in text.encode("utf-16le"):
        value ^= byte
        value = (value * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return value

def stable_id(prefix: str, payload: str) -> str:
    return f"{prefix}_{fnv1a64_utf16le(payload):016x}"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha256_lines(lines) -> str:
    return sha256_text("\n".join(str(x) for x in lines) + "\n")

def cfloat(value: float, digits: int = 10) -> str:
    if not math.isfinite(value):
        raise ValueError("non-finite numeric value")
    if value == 0.0:
        value = 0.0
    return f"{value:.{digits}f}"

def cbool(value: bool) -> str:
    return "true" if value else "false"
