from __future__ import annotations

FNV1A_64_OFFSET = 14695981039346656037
FNV1A_64_PRIME = 1099511628211
MASK64 = (1 << 64) - 1

def fnv1a64_utf16le(value: str) -> int:
    result = FNV1A_64_OFFSET
    for byte in value.encode("utf-16le"):
        result ^= byte
        result = (result * FNV1A_64_PRIME) & MASK64
    return result

def stable_id(prefix: str, canonical_payload: str) -> str:
    return f"{prefix}_{fnv1a64_utf16le(canonical_payload):016x}"
