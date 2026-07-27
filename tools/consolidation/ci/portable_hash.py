"""Cross-platform text hash verification for LF/CRLF Git checkouts."""
from __future__ import annotations

import hashlib
from pathlib import Path


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_variants(path: Path) -> set[str]:
    raw = path.read_bytes()
    variants = {_digest(raw)}
    if b"\x00" in raw[:4096]:
        return variants
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if had_bom else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return variants
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for newline in ("\n", "\r\n"):
        payload = normalized.replace("\n", newline).encode("utf-8")
        variants.add(_digest(payload))
        variants.add(_digest(b"\xef\xbb\xbf" + payload))
    return variants


def canonical_sha256(path: Path) -> str:
    """Hash UTF-8 text in its LF canonical form; keep binary bytes exact."""
    raw = path.read_bytes()
    if b"\x00" in raw[:4096]:
        return _digest(raw)
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if had_bom else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return _digest(raw)
    payload = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return _digest((b"\xef\xbb\xbf" if had_bom else b"") + payload)


def hash_matches(path: Path, expected: str) -> bool:
    return expected.lower() in sha256_variants(path)
