from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .errors import IntegrityError


# Closed classification registry. Unknown files are treated conservatively: they are
# text only when UTF-8 decoding succeeds and the payload contains no NUL byte.
_TEXT_EXTENSIONS = frozenset(
    {
        "",
        ".cfg",
        ".conf",
        ".csv",
        ".env",
        ".gitattributes",
        ".gitignore",
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

_PATH_KEYS = (
    "path",
    "relative_path",
    "root_relative_path",
    "repo_relative_path",
    "artifact_path",
)
_HASH_KEYS = (
    "sha256",
    "content_sha256",
    "file_sha256",
    "raw_sha256",
)
_RECORD_CONTAINER_KEYS = (
    "records",
    "artifacts",
    "files",
    "entries",
)


@dataclass(frozen=True)
class VerificationSummary:
    record_count: int
    raw_match_count: int
    canonical_text_match_count: int
    mismatch_count: int

    def as_dict(self) -> dict[str, int | bool]:
        return {
            "record_count": self.record_count,
            "raw_match_count": self.raw_match_count,
            "canonical_text_match_count": self.canonical_text_match_count,
            "mismatch_count": self.mismatch_count,
            "passed": self.mismatch_count == 0,
        }


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"baseline manifest load failed path={path}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise IntegrityError(f"baseline manifest must be an object path={path}")
    return value


def _manifest_path(package_root: Path) -> Path:
    direct = package_root / "baseline_manifest.json"
    if direct.is_file():
        return direct

    matches = sorted(package_root.rglob("baseline_manifest.json"))
    if len(matches) != 1:
        raise IntegrityError(
            "baseline manifest resolution failed "
            f"package_root={package_root} candidate_count={len(matches)}"
        )
    return matches[0]


def _records(manifest: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    for key in _RECORD_CONTAINER_KEYS:
        value = manifest.get(key)
        if isinstance(value, list):
            if not all(isinstance(item, Mapping) for item in value):
                raise IntegrityError(f"baseline manifest field {key!r} contains non-object records")
            return value
    raise IntegrityError(
        "baseline manifest has no supported record collection; "
        f"expected one of {_RECORD_CONTAINER_KEYS}"
    )


def _record_value(record: Mapping[str, Any], keys: Iterable[str], label: str) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise IntegrityError(f"baseline record missing {label}: keys={tuple(keys)} record={dict(record)}")


def _record_path(record: Mapping[str, Any]) -> str:
    return _record_value(record, _PATH_KEYS, "path")


def _normalize_sha256_reference(value: str) -> str:
    """Normalize supported SHA-256 reference forms to a bare lowercase digest.

    LCM-00 baseline manifests use the URI-like form ``sha256:<64-hex>`` while
    some focused fixtures use the bare ``<64-hex>`` form. Both representations
    denote the same digest and are accepted. No other algorithm, nested prefix,
    whitespace inside the digest, or non-hex payload is accepted.
    """

    normalized = value.strip().lower()
    prefix = "sha256:"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix):]

    if len(normalized) != 64 or any(
        character not in "0123456789abcdef" for character in normalized
    ):
        raise IntegrityError(f"baseline record has invalid sha256 value={value!r}")
    return normalized


def _record_sha256(record: Mapping[str, Any]) -> str:
    value = _record_value(record, _HASH_KEYS, "sha256")
    return _normalize_sha256_reference(value)


def _resolve_repo_path(repo_root: Path, relative_path: str) -> Path:
    candidate_path = Path(relative_path)
    if not relative_path or candidate_path.is_absolute():
        raise IntegrityError(f"baseline path is empty or absolute path={relative_path!r}")

    resolved_root = repo_root.resolve()
    resolved = (resolved_root / candidate_path).resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise IntegrityError(f"baseline path escapes repository path={relative_path!r}") from exc
    return resolved


def _looks_like_text(path: Path, data: bytes) -> bool:
    suffix = path.suffix.lower()
    if suffix in _BINARY_EXTENSIONS:
        return False
    if b"\x00" in data[:65536]:
        return False
    if suffix in _TEXT_EXTENSIONS:
        try:
            data.decode("utf-8-sig")
        except UnicodeDecodeError:
            return False
        return True
    try:
        data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    return True


def canonicalize_text_eol(data: bytes) -> bytes:
    """Return a byte-stable LF representation without altering other text bytes.

    Git's Windows checkout can materialize LF repository blobs as CRLF working-tree
    files when core.autocrlf=true. Only line-ending bytes are normalized here. The
    function does not trim whitespace, change encoding, normalize Unicode, or alter
    a final newline.
    """

    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def verify_repository_bytes_cross_platform(
    repo_root: Path | str,
    package_root: Path | str,
) -> dict[str, int | bool]:
    """Verify the LCM-00 baseline against a platform-specific working tree.

    Raw SHA-256 remains authoritative. A text file is accepted after raw mismatch
    only when LF canonicalization alone reproduces the frozen baseline SHA-256.
    Binary files never receive canonicalization. Unknown, missing, symlinked, path-
    escaping, or semantically modified files remain fail-closed.
    """

    resolved_repo = Path(repo_root).resolve()
    resolved_package = Path(package_root).resolve()
    manifest = _read_json(_manifest_path(resolved_package))
    records = _records(manifest)

    raw_match_count = 0
    canonical_text_match_count = 0
    mismatch_count = 0
    mismatch_examples: list[dict[str, str]] = []

    for record in records:
        relative_path = _record_path(record)
        expected_sha256 = _record_sha256(record)

        try:
            target = _resolve_repo_path(resolved_repo, relative_path)
        except IntegrityError as exc:
            mismatch_count += 1
            if len(mismatch_examples) < 20:
                mismatch_examples.append(
                    {"path": relative_path, "reason": "PATH_ESCAPE", "detail": str(exc)}
                )
            continue

        if target.is_symlink():
            mismatch_count += 1
            if len(mismatch_examples) < 20:
                mismatch_examples.append({"path": relative_path, "reason": "SYMLINK_DENIED"})
            continue
        if not target.is_file():
            mismatch_count += 1
            if len(mismatch_examples) < 20:
                mismatch_examples.append({"path": relative_path, "reason": "MISSING"})
            continue

        try:
            current = target.read_bytes()
        except OSError as exc:
            mismatch_count += 1
            if len(mismatch_examples) < 20:
                mismatch_examples.append(
                    {"path": relative_path, "reason": "READ_FAILED", "detail": str(exc)}
                )
            continue

        if _sha256(current) == expected_sha256:
            raw_match_count += 1
            continue

        if _looks_like_text(target, current):
            canonical = canonicalize_text_eol(current)
            if canonical != current and _sha256(canonical) == expected_sha256:
                canonical_text_match_count += 1
                continue

        mismatch_count += 1
        if len(mismatch_examples) < 20:
            mismatch_examples.append({"path": relative_path, "reason": "HASH_MISMATCH"})

    summary = VerificationSummary(
        record_count=len(records),
        raw_match_count=raw_match_count,
        canonical_text_match_count=canonical_text_match_count,
        mismatch_count=mismatch_count,
    )
    if mismatch_count:
        raise IntegrityError(
            "baseline repository mismatch "
            f"count={mismatch_count} first={mismatch_examples[:3]}"
        )
    return summary.as_dict()
