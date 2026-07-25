"""Shared fail-closed integrity primitives for LCM reference packages.

Raw bytes remain the primary authority.  A digest mismatch may be accepted only
for UTF-8 text when the expected digest and size exactly match the same bytes
materialized with all-LF or all-CRLF line endings.  No whitespace, Unicode,
encoding, or final-newline normalization is performed.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


class IntegrityError(RuntimeError):
    """Raised when an integrity claim cannot be proven exactly."""


_SHA256 = re.compile(r"^(?:sha256:)?([0-9a-fA-F]{64})$")
_TEXT_EXTENSIONS = frozenset(
    {
        "",
        ".cfg",
        ".conf",
        ".csv",
        ".env",
        ".ini",
        ".json",
        ".jsonl",
        ".md",
        ".mq5",
        ".mqh",
        ".ps1",
        ".py",
        ".pyi",
        ".rst",
        ".sh",
        ".toml",
        ".tsv",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)
_BINARY_EXTENSIONS = frozenset(
    {
        ".7z",
        ".bin",
        ".bmp",
        ".dll",
        ".doc",
        ".docx",
        ".ex5",
        ".exe",
        ".gif",
        ".gz",
        ".ico",
        ".jar",
        ".jpeg",
        ".jpg",
        ".mp3",
        ".mp4",
        ".pdf",
        ".png",
        ".ppt",
        ".pptx",
        ".pyc",
        ".so",
        ".tar",
        ".webp",
        ".xls",
        ".xlsx",
        ".zip",
    }
)


@dataclass(frozen=True)
class DigestMatch:
    mode: str
    expected_sha256: str
    actual_sha256: str
    materialized_size_bytes: int

    @property
    def match_mode(self) -> str:
        """Compatibility name used by phase-local verification reports."""

        return self.mode


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def normalize_sha256(value: str) -> str:
    if not isinstance(value, str):
        raise IntegrityError(f"sha256 reference must be a string: {value!r}")
    match = _SHA256.fullmatch(value.strip())
    if match is None:
        raise IntegrityError(f"invalid sha256 reference: {value!r}")
    return "sha256:" + match.group(1).lower()


def canonical_json_digest(value: Any, omit_field: str | None = None) -> str:
    if omit_field and isinstance(value, Mapping):
        value = {key: item for key, item in value.items() if key != omit_field}
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _sha256(payload)


def object_digest(value: Any, omit_field: str | None = None) -> str:
    """Public concise alias for canonical JSON object/list digests."""

    return canonical_json_digest(value, omit_field)


def canonicalize_text_eol(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def materialize_text_crlf(data: bytes) -> bytes:
    return canonicalize_text_eol(data).replace(b"\n", b"\r\n")


def _looks_like_text(path: Path, data: bytes) -> bool:
    suffix = path.suffix.lower()
    if suffix in _BINARY_EXTENSIONS or b"\x00" in data[:65536]:
        return False
    if suffix not in _TEXT_EXTENSIONS:
        return False
    try:
        data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    return True


def verify_file_digest(
    path: Path,
    expected_sha256: str,
    expected_size_bytes: int | None = None,
) -> DigestMatch:
    """Verify one file, permitting only symmetric UTF-8 text EOL equivalence."""

    expected = normalize_sha256(expected_sha256)
    if path.is_symlink():
        raise IntegrityError(f"symlink denied: {path}")
    if not path.is_file():
        raise IntegrityError(f"file missing: {path}")
    try:
        current = path.read_bytes()
    except OSError as exc:
        raise IntegrityError(f"file read failed: {path}: {exc}") from exc

    candidates: list[tuple[str, bytes]] = [("raw", current)]
    if _looks_like_text(path, current):
        candidates.extend(
            (
                ("canonical_lf", canonicalize_text_eol(current)),
                ("canonical_crlf", materialize_text_crlf(current)),
            )
        )

    for mode, materialized in candidates:
        if _sha256(materialized) != expected:
            continue
        if expected_size_bytes is not None and len(materialized) != expected_size_bytes:
            raise IntegrityError(
                f"size mismatch: {path} expected={expected_size_bytes} "
                f"materialized={len(materialized)} mode={mode}"
            )
        return DigestMatch(
            mode=mode,
            expected_sha256=expected,
            actual_sha256=_sha256(current),
            materialized_size_bytes=len(materialized),
        )

    modes = {mode: _sha256(data) for mode, data in candidates}
    raise IntegrityError(
        f"digest mismatch: {path} expected={expected} candidates={modes}"
    )


def _safe_manifest_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise IntegrityError(f"invalid manifest path: {relative!r}")
    posix = PurePosixPath(relative)
    if posix.is_absolute() or any(part in {"", ".", ".."} for part in posix.parts):
        raise IntegrityError(f"unsafe manifest path: {relative!r}")
    resolved_root = root.resolve()
    resolved = (resolved_root / Path(*posix.parts)).resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise IntegrityError(f"manifest path escapes package: {relative!r}") from exc
    return resolved


def resolve_relative_path(root: Path, relative: str, label: str = "path") -> Path:
    """Resolve a POSIX repository-relative path without allowing traversal."""

    try:
        return _safe_manifest_path(root, relative)
    except IntegrityError as exc:
        raise IntegrityError(f"unsafe {label}: {relative!r}: {exc}") from exc


def verify_output_manifest(
    root: Path,
    manifest: Mapping[str, Any],
    manifest_name: str = "output_manifest.json",
) -> dict[str, int | bool]:
    """Verify manifest self-digest, exact file set, sizes, and content digests."""

    rows = manifest.get("files")
    if not isinstance(rows, list) or not all(isinstance(row, Mapping) for row in rows):
        raise IntegrityError("manifest files must be a list of objects")
    if manifest.get("file_count") != len(rows):
        raise IntegrityError(
            f"manifest file_count mismatch: {manifest.get('file_count')} != {len(rows)}"
        )
    stored_digest = manifest.get("manifest_digest")
    if stored_digest is not None and canonical_json_digest(manifest, "manifest_digest") != normalize_sha256(stored_digest):
        raise IntegrityError("manifest self-digest mismatch")

    listed: set[str] = set()
    mode_counts = {"raw": 0, "canonical_lf": 0, "canonical_crlf": 0}
    for row in rows:
        relative = row.get("path")
        if relative in listed:
            raise IntegrityError(f"duplicate manifest path: {relative!r}")
        listed.add(relative)
        expected_size = row.get("size_bytes")
        if not isinstance(expected_size, int) or expected_size < 0:
            raise IntegrityError(f"invalid manifest size: {relative!r}")
        match = verify_file_digest(
            _safe_manifest_path(root, relative),
            row.get("sha256"),
            expected_size,
        )
        mode_counts[match.mode] += 1

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).as_posix() != manifest_name
    }
    if actual != listed:
        missing = sorted(listed - actual)
        unexpected = sorted(actual - listed)
        raise IntegrityError(
            f"manifest file-set mismatch missing={missing[:10]} unexpected={unexpected[:10]}"
        )
    return {
        "passed": True,
        "file_count": len(rows),
        "raw_match_count": mode_counts["raw"],
        "canonical_lf_match_count": mode_counts["canonical_lf"],
        "canonical_crlf_match_count": mode_counts["canonical_crlf"],
        "text_eol_equivalent_match_count": (
            mode_counts["canonical_lf"] + mode_counts["canonical_crlf"]
        ),
    }


def verify_manifest(
    root: Path,
    manifest: Mapping[str, Any],
    manifest_name: str = "output_manifest.json",
) -> dict[str, int | bool]:
    """Compatibility wrapper with the phase-report aggregate field."""

    result = verify_output_manifest(root, manifest, manifest_name)
    return {
        **result,
        "eol_equivalent_match_count": result[
            "text_eol_equivalent_match_count"
        ],
    }


def verify_object_digest(value: Mapping[str, Any], digest_field: str) -> None:
    stored = value.get(digest_field)
    if canonical_json_digest(value, digest_field) != normalize_sha256(stored):
        raise IntegrityError(f"object self-digest mismatch: {digest_field}")


def verify_pre_receipt_manifest_link(
    manifest: Mapping[str, Any],
    receipt: Mapping[str, Any],
    receipt_path: str,
) -> None:
    """Verify the deliberate two-pass manifest/receipt publication protocol."""

    verify_object_digest(receipt, "receipt_digest")
    reconstructed = copy.deepcopy(dict(manifest))
    rows = reconstructed.get("files")
    if not isinstance(rows, list):
        raise IntegrityError("manifest files missing while verifying receipt link")
    filtered = [row for row in rows if row.get("path") != receipt_path]
    if len(filtered) != len(rows) - 1:
        raise IntegrityError(f"receipt path not represented exactly once: {receipt_path}")
    reconstructed["files"] = filtered
    reconstructed["file_count"] = len(filtered)
    reconstructed["manifest_digest"] = canonical_json_digest(
        reconstructed, "manifest_digest"
    )
    serialized = (
        json.dumps(reconstructed, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    expected = normalize_sha256(receipt.get("output_manifest_digest"))
    if _sha256(serialized) != expected:
        raise IntegrityError("receipt does not bind the pre-receipt manifest")


def verify_receipt_binding(
    manifest: Mapping[str, Any],
    receipt: Mapping[str, Any],
    receipt_path: str,
    handoff_digest: str | None = None,
) -> None:
    """Verify receipt self/linkage plus an optional handoff reference."""

    verify_pre_receipt_manifest_link(manifest, receipt, receipt_path)
    if handoff_digest is not None and normalize_sha256(
        receipt.get("handoff_digest")
    ) != normalize_sha256(handoff_digest):
        raise IntegrityError("receipt handoff digest mismatch")
