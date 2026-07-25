from __future__ import annotations

import hashlib
from pathlib import Path

_TEXT_SUFFIXES = frozenset(
    {
        ".bat",
        ".cfg",
        ".csv",
        ".ini",
        ".json",
        ".jsonl",
        ".md",
        ".mq4",
        ".mq5",
        ".mqh",
        ".ps1",
        ".py",
        ".toml",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)


def _sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def normalize_repository_text(payload: bytes) -> bytes:
    """Return platform-independent repository text bytes.

    Git checkouts on Windows may materialize LF-controlled repository text as
    CRLF. LCM source bindings are content bindings, not checkout-format
    bindings, so textual sources are normalized to UTF-8/LF before hashing.
    A UTF-8 BOM is retained because it is source content; only newline encoding
    is normalized.
    """

    return payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def source_binding_digest(path: Path) -> str:
    """Compute the cross-platform digest used for legacy source bindings."""

    payload = path.read_bytes()
    if path.suffix.lower() in _TEXT_SUFFIXES:
        payload = normalize_repository_text(payload)
    return _sha256(payload)


def source_binding_matches(path: Path, expected_digest: str) -> bool:
    """Return True when the working-tree source matches its frozen binding."""

    return source_binding_digest(path) == expected_digest
