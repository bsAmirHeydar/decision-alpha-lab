"""Cross-language identity hashing and strong evidence digests."""
from __future__ import annotations
import hashlib
from typing import Any
from .codec import canonical_utf8

FNV1A64_OFFSET=0xCBF29CE484222325
FNV1A64_PRIME=0x100000001B3
MASK64=0xFFFFFFFFFFFFFFFF


def fnv1a64(data: bytes) -> int:
    value=FNV1A64_OFFSET
    for byte in data:
        value ^= byte
        value = (value * FNV1A64_PRIME) & MASK64
    return value


def fnv1a64_hex(data: bytes) -> str:
    return f"{fnv1a64(data):016x}"


def canonical_id_digest(value: Any) -> str:
    return fnv1a64_hex(canonical_utf8(value))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_utf8(value))
