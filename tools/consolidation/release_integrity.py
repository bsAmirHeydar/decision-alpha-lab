from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

SHA256_RE = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")
AUTHORITY_FIELDS = (
    "semantic_change",
    "semantic_merge_authority",
    "deletion_authority",
    "runtime_authority",
    "order_authority",
    "capital_authority",
    "runtime_authority_created",
    "order_authority_created",
    "capital_authority_created",
)
BINARY_SUFFIXES = {
    ".7z",
    ".bin",
    ".bmp",
    ".dll",
    ".doc",
    ".docx",
    ".ex5",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".pyc",
    ".pyo",
    ".tar",
    ".webp",
    ".xlsx",
    ".zip",
}


@dataclass(frozen=True)
class ReleaseIntegrityPolicy:
    policy_id: str
    historical_stage: str
    immutable_prefixes: tuple[str, ...]
    immutable_exact_paths: tuple[str, ...]
    amendment_search_roots: tuple[str, ...]
    legacy_amendment_documents: tuple[str, ...]
    require_all_index_targets: bool

    def is_immutable(self, relative: str) -> bool:
        normalized = relative.replace("\\", "/")
        return normalized in self.immutable_exact_paths or any(
            normalized.startswith(prefix) for prefix in self.immutable_prefixes
        )


@dataclass(frozen=True)
class AmendmentRecord:
    source_document: str
    path: str
    previous_sha256: str
    current_sha256: str
    semantic_change: bool
    runtime_authority_created: bool
    order_authority_created: bool
    capital_authority_created: bool


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def _canonical_document_digest(value: dict[str, Any], field: str) -> str:
    payload = json.dumps(
        {key: item for key, item in value.items() if key != field},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _strip_sha256(value: str) -> str:
    return value.removeprefix("sha256:").lower()


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _looks_textual(path: Path, payload: bytes) -> bool:
    if path.suffix.lower() in BINARY_SUFFIXES or b"\x00" in payload:
        return False
    try:
        payload.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    return True


def canonical_repository_bytes(path: Path) -> bytes:
    """Return platform-stable bytes for repository text while preserving binary bytes.

    Git checkouts may materialize text with CRLF even when the canonical repository blob and
    release ZIP use LF. Historical release integrity is about content, not checkout line endings.
    UTF-8 BOMs are intentionally preserved; only newline representation is normalized.
    """

    payload = path.read_bytes()
    if not _looks_textual(path, payload):
        return payload
    return payload.replace(b"\r\n", b"\n")


def canonical_repository_sha256(path: Path) -> str:
    return "sha256:" + _sha256(canonical_repository_bytes(path))


def digest_matches_path(path: Path, expected: str) -> bool:
    if not SHA256_RE.fullmatch(expected):
        return False
    payload = path.read_bytes()
    expected_raw = _strip_sha256(expected)
    if _sha256(payload) == expected_raw:
        return True
    if _looks_textual(path, payload):
        canonical = payload.replace(b"\r\n", b"\n")
        return _sha256(canonical) == expected_raw
    return False


def _validate_schema(instance_path: Path, schema_path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        instance = _read_json(instance_path)
        schema = _read_json(schema_path)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for issue in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
            location = "/".join(str(item) for item in issue.path) or "<root>"
            errors.append(
                f"schema violation {instance_path.as_posix()} at {location}: {issue.message}"
            )
        return instance
    except Exception as exc:
        errors.append(f"schema validation failed for {instance_path.as_posix()}: {exc}")
        return None


def load_policy(repo: Path, policy_path: Path, schema_path: Path, errors: list[str]) -> ReleaseIntegrityPolicy | None:
    document = _validate_schema(repo / policy_path, repo / schema_path, errors)
    if document is None:
        return None
    if document.get("status") != "ACTIVE":
        errors.append(f"release integrity policy is not ACTIVE: {policy_path.as_posix()}")
    for field in AUTHORITY_FIELDS:
        if document.get(field) is True:
            errors.append(f"release integrity policy grants forbidden authority: {field}")
    digest = document.get("document_digest")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append(f"missing or invalid document_digest: {policy_path.as_posix()}")
    elif digest != _canonical_document_digest(document, "document_digest"):
        errors.append(f"document_digest mismatch: {policy_path.as_posix()}")
    return ReleaseIntegrityPolicy(
        policy_id=str(document.get("policy_id", "")),
        historical_stage=str(document.get("historical_stage", "")),
        immutable_prefixes=tuple(str(item) for item in document.get("immutable_prefixes", [])),
        immutable_exact_paths=tuple(str(item) for item in document.get("immutable_exact_paths", [])),
        amendment_search_roots=tuple(str(item) for item in document.get("amendment_search_roots", [])),
        legacy_amendment_documents=tuple(
            str(item) for item in document.get("legacy_amendment_documents", [])
        ),
        require_all_index_targets=bool(document.get("require_all_index_targets", True)),
    )


def _iter_amendment_paths(repo: Path, policy: ReleaseIntegrityPolicy) -> Iterable[Path]:
    seen: set[str] = set()
    for relative in policy.legacy_amendment_documents:
        normalized = relative.replace("\\", "/")
        if normalized not in seen:
            seen.add(normalized)
            yield repo / normalized
    for root_relative in policy.amendment_search_roots:
        root = repo / root_relative
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.json")):
            normalized = path.relative_to(repo).as_posix()
            if normalized not in seen:
                seen.add(normalized)
                yield path


def _validate_amendment_document(
    repo: Path,
    path: Path,
    generic_schema_path: Path,
    errors: list[str],
) -> list[AmendmentRecord]:
    relative = path.relative_to(repo).as_posix()
    if not path.is_file():
        errors.append(f"release amendment document missing: {relative}")
        return []
    try:
        document = _read_json(path)
    except Exception as exc:
        errors.append(f"invalid release amendment document {relative}: {exc}")
        return []

    schema_ref = str(document.get("$schema", ""))
    if "ci_recovery_release_amendment.schema.json" in schema_ref:
        legacy_schema = (path.parent / schema_ref).resolve()
        validated = _validate_schema(path, legacy_schema, errors)
    else:
        validated = _validate_schema(path, repo / generic_schema_path, errors)
    if validated is None:
        return []
    document = validated

    digest_field = "amendment_digest" if "amendment_digest" in document else "document_digest"
    digest = document.get(digest_field)
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append(f"missing or invalid {digest_field}: {relative}")
    elif digest != _canonical_document_digest(document, digest_field):
        errors.append(f"{digest_field} mismatch: {relative}")

    if document.get("status") != "PASS":
        errors.append(f"release amendment is not PASS: {relative}")
    for field in AUTHORITY_FIELDS:
        if document.get(field) is True:
            errors.append(f"release amendment grants forbidden authority: {relative}: {field}")

    rows = document.get("records", [])
    if not isinstance(rows, list) or document.get("record_count") != len(rows):
        errors.append(f"release amendment record count mismatch: {relative}")
        return []

    output: list[AmendmentRecord] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"non-object release amendment row: {relative}:{index}")
            continue
        row_path = str(row.get("path", "")).replace("\\", "/")
        previous = str(row.get("previous_sha256", ""))
        current = str(row.get("current_sha256", ""))
        if not row_path or row_path.startswith("/") or ".." in Path(row_path).parts:
            errors.append(f"invalid release amendment path: {relative}:{index}:{row_path!r}")
            continue
        if not SHA256_RE.fullmatch(previous) or not SHA256_RE.fullmatch(current):
            errors.append(f"invalid release amendment digest: {relative}:{index}:{row_path}")
            continue
        forbidden = [field for field in AUTHORITY_FIELDS if row.get(field) is True]
        if forbidden:
            errors.append(
                f"release amendment row grants forbidden authority: {relative}:{index}:{forbidden}"
            )
        output.append(
            AmendmentRecord(
                source_document=relative,
                path=row_path,
                previous_sha256="sha256:" + _strip_sha256(previous),
                current_sha256="sha256:" + _strip_sha256(current),
                semantic_change=bool(row.get("semantic_change", False)),
                runtime_authority_created=bool(row.get("runtime_authority_created", False)),
                order_authority_created=bool(row.get("order_authority_created", False)),
                capital_authority_created=bool(row.get("capital_authority_created", False)),
            )
        )
    return output


def load_amendments(
    repo: Path,
    policy: ReleaseIntegrityPolicy,
    generic_schema_path: Path,
    errors: list[str],
) -> dict[str, list[AmendmentRecord]]:
    output: dict[str, list[AmendmentRecord]] = {}
    for path in _iter_amendment_paths(repo, policy):
        for record in _validate_amendment_document(repo, path, generic_schema_path, errors):
            output.setdefault(record.path, []).append(record)
    return output


def resolve_amendment_chain(
    path: str,
    baseline_sha256: str,
    records: list[AmendmentRecord],
    errors: list[str],
) -> str:
    current = "sha256:" + _strip_sha256(baseline_sha256)
    remaining = list(records)
    visited: set[tuple[str, str]] = set()
    while True:
        candidates = [record for record in remaining if record.previous_sha256 == current]
        if not candidates:
            break
        if len(candidates) > 1:
            errors.append(f"release amendment fork detected: {path}: {current}")
            break
        record = candidates[0]
        edge = (record.previous_sha256, record.current_sha256)
        if edge in visited or record.previous_sha256 == record.current_sha256:
            errors.append(f"release amendment cycle or no-op detected: {path}: {edge}")
            break
        visited.add(edge)
        current = record.current_sha256
        remaining.remove(record)
    if remaining:
        details = [
            f"{record.source_document}:{record.previous_sha256}->{record.current_sha256}"
            for record in remaining
        ]
        errors.append(f"orphaned release amendment records: {path}: {details}")
    return current


def verify_historical_release_snapshot(
    repo: Path,
    *,
    release_root: Path,
    policy_path: Path,
    policy_schema_path: Path,
    amendment_schema_path: Path,
) -> list[str]:
    errors: list[str] = []
    policy = load_policy(repo, policy_path, policy_schema_path, errors)
    if policy is None:
        return errors

    release = repo / release_root
    required = {
        "README.md",
        "INSTALL.md",
        "ROLLBACK.md",
        "COMMIT_MESSAGE.txt",
        "APPLY.ps1",
        "PATCH_MANIFEST.json",
        "PATCH_FILE_INDEX.txt",
        "PATCH_FILE_HASHES.sha256",
        "QA_REPORT.json",
    }
    if not release.is_dir():
        errors.append(f"release directory missing: {release_root.as_posix()}")
        return errors
    present = {item.name for item in release.iterdir() if item.is_file()}
    missing = sorted(required - present)
    if missing:
        errors.append(f"release controls missing: {missing}")
        return errors

    index_path = release / "PATCH_FILE_INDEX.txt"
    ledger_path = release / "PATCH_FILE_HASHES.sha256"
    index = [
        line.strip().replace("\\", "/")
        for line in index_path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if index != sorted(set(index)):
        errors.append("patch file index is not sorted and unique")
    if policy.require_all_index_targets:
        for relative in index:
            if not (repo / relative).is_file():
                errors.append(f"patch index target missing: {relative}")

    ledger: dict[str, str] = {}
    for line in ledger_path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid patch hash line: {line}")
            continue
        normalized = relative.replace("\\", "/")
        if normalized in ledger:
            errors.append(f"duplicate patch hash path: {normalized}")
            continue
        if not SHA256_RE.fullmatch(digest):
            errors.append(f"invalid patch hash digest: {normalized}: {digest}")
            continue
        ledger[normalized] = "sha256:" + _strip_sha256(digest)

    expected_hashed = set(index) - {f"{release_root.as_posix()}/PATCH_FILE_HASHES.sha256"}
    if set(ledger) != expected_hashed:
        errors.append("patch hash ledger paths do not match the patch index")

    amendments = load_amendments(repo, policy, amendment_schema_path, errors)
    immutable_count = 0
    evolvable_count = 0
    for relative, baseline in ledger.items():
        target = repo / relative
        if not target.is_file():
            continue
        if not policy.is_immutable(relative):
            evolvable_count += 1
            # Historical delivery records prove what was shipped. Active implementation bytes are
            # governed by current tests, current schemas and explicit semantic freezes, not by a
            # permanent equality check against an old patch snapshot.
            continue
        immutable_count += 1
        terminal = resolve_amendment_chain(relative, baseline, amendments.get(relative, []), errors)
        if not digest_matches_path(target, terminal):
            errors.append(f"immutable release artifact hash mismatch: {relative}")

    immutable_amendment_paths = {
        relative for relative in amendments if policy.is_immutable(relative)
    }
    unknown_immutable_amendments = immutable_amendment_paths - set(ledger)
    if unknown_immutable_amendments:
        errors.append(
            "immutable release amendments reference paths outside the historical ledger: "
            + repr(sorted(unknown_immutable_amendments))
        )

    manifest = _read_json(release / "PATCH_MANIFEST.json")
    if manifest.get("patch_file_count") != len(index):
        errors.append("patch manifest file count mismatch")
    authority = manifest.get("authority", {})
    if isinstance(authority, dict):
        for field in AUTHORITY_FIELDS:
            if authority.get(field) is True:
                errors.append(f"release manifest grants forbidden authority: {field}")

    if immutable_count == 0:
        errors.append("release integrity policy classifies zero W0 artifacts as immutable")
    if evolvable_count == 0:
        errors.append("release integrity policy classifies zero W0 artifacts as evolvable")
    return errors
