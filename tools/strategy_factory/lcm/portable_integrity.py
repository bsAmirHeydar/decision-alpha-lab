from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

LCM16A_AUDIT_RELATIVE = Path(
    "registry/legacy_context_migration/full_system_audits/"
    "CLOSUREAUDIT_5EEC97304039BFF3AAAFB57605961BA2"
)
BASELINE_DOCUMENT = "baseline_amendment.json"
BASELINE_RECORDS = "records/baseline_amendments.jsonl"
EXPECTED_AMENDMENT_COUNT = 242


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _normalise_expected(expected: str) -> str:
    value = expected.strip().lower()
    return value if value.startswith("sha256:") else "sha256:" + value


def _stream_digest_variants(path: Path) -> tuple[frozenset[str], str]:
    """Return raw/LF/CRLF SHA-256 variants without loading large files.

    UTF-8 validity and NUL detection are checked incrementally. Binary or
    non-UTF-8 payloads expose only the raw digest. A pending CR is carried
    across chunk boundaries so CRLF pairs are canonicalised correctly.
    """
    import codecs

    raw = hashlib.sha256()
    lf_hash = hashlib.sha256()
    crlf_hash = hashlib.sha256()
    decoder = codecs.getincrementaldecoder("utf-8-sig")()
    text_candidate = True
    pending_cr = False

    def emit_lf_normalised(data: bytes) -> None:
        nonlocal pending_cr
        output = bytearray()
        for byte in data:
            if pending_cr:
                output.append(0x0A)
                pending_cr = False
                if byte == 0x0A:
                    continue
            if byte == 0x0D:
                pending_cr = True
            else:
                output.append(byte)
        if output:
            payload = bytes(output)
            lf_hash.update(payload)
            crlf_hash.update(payload.replace(b"\n", b"\r\n"))

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            raw.update(chunk)
            if not text_candidate:
                continue
            if b"\x00" in chunk:
                text_candidate = False
                continue
            try:
                decoder.decode(chunk, final=False)
            except UnicodeDecodeError:
                text_candidate = False
                continue
            emit_lf_normalised(chunk)

    raw_digest = "sha256:" + raw.hexdigest()
    if not text_candidate:
        return frozenset({raw_digest}), raw_digest
    try:
        decoder.decode(b"", final=True)
    except UnicodeDecodeError:
        return frozenset({raw_digest}), raw_digest
    if pending_cr:
        lf_hash.update(b"\n")
        crlf_hash.update(b"\r\n")
    lf_digest = "sha256:" + lf_hash.hexdigest()
    crlf_digest = "sha256:" + crlf_hash.hexdigest()
    return frozenset({raw_digest, lf_digest, crlf_digest}), lf_digest


def digest_variants(path: Path) -> frozenset[str]:
    return _stream_digest_variants(path)[0]


def matches_expected_digest(path: Path, expected: str) -> bool:
    if not path.is_file():
        return False
    return _normalise_expected(expected) in digest_variants(path)


def portable_file_digest(path: Path) -> str:
    """Return LF-canonical SHA-256 for UTF-8 text and raw SHA-256 for binary."""
    return _stream_digest_variants(path)[1]

def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def _manifest_entries(package_root: Path) -> dict[str, dict[str, Any]]:
    manifest_path = package_root / "output_manifest.json"
    if not manifest_path.is_file():
        raise ValueError("LCM-16A output manifest is missing")
    manifest = _load_json(manifest_path)
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("LCM-16A output manifest files are malformed")
    entries: dict[str, dict[str, Any]] = {}
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError("LCM-16A output manifest entry is malformed")
        entries[item["path"]] = item
    return entries


def load_verified_lcm16a_amendments(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Load the exact bound LCM-16A amendment set.

    The amendment package is optional for older phase-only checkouts. When it
    exists, both amendment artifacts must be bound by the LCM-16A output
    manifest and all records must remain scoped to AIEOS with authority false.
    """
    package_root = repo_root / LCM16A_AUDIT_RELATIVE
    document_path = package_root / BASELINE_DOCUMENT
    records_path = package_root / BASELINE_RECORDS
    if not document_path.is_file() and not records_path.is_file():
        return {}
    if not document_path.is_file() or not records_path.is_file():
        raise ValueError("partial LCM-16A baseline amendment package")

    entries = _manifest_entries(package_root)
    for relative, path in (
        (BASELINE_DOCUMENT, document_path),
        (BASELINE_RECORDS, records_path),
    ):
        entry = entries.get(relative)
        if not entry or not isinstance(entry.get("sha256"), str):
            raise ValueError(f"LCM-16A output manifest does not bind {relative}")
        if not matches_expected_digest(path, entry["sha256"]):
            raise ValueError(f"LCM-16A bound amendment hash mismatch: {relative}")

    document = _load_json(document_path)
    records = _load_jsonl(records_path)
    expected_count = document.get("amendment_count", EXPECTED_AMENDMENT_COUNT)
    if expected_count != EXPECTED_AMENDMENT_COUNT or len(records) != EXPECTED_AMENDMENT_COUNT:
        raise ValueError("unexpected LCM-16A amendment count")

    amendments: dict[str, dict[str, Any]] = {}
    for row in records:
        path = row.get("candidate_path")
        previous = row.get("previous_sha256")
        amended = row.get("amended_sha256")
        if not isinstance(path, str) or not path.startswith("docs/ai_algorithm_engineering_os/"):
            raise ValueError(f"unapproved LCM-16A amendment scope: {path}")
        if path in amendments:
            raise ValueError(f"duplicate LCM-16A amendment path: {path}")
        if not isinstance(previous, str) or not previous.startswith("sha256:"):
            raise ValueError(f"invalid previous digest: {path}")
        if not isinstance(amended, str) or not amended.startswith("sha256:"):
            raise ValueError(f"invalid amended digest: {path}")
        if previous == amended:
            raise ValueError(f"non-changing LCM-16A amendment: {path}")
        for flag in (
            "deletion_approved",
            "deletion_performed",
            "runtime_authority_created",
            "live_order_authority_created",
            "capital_authority_created",
        ):
            if row.get(flag, False):
                raise ValueError(f"LCM-16A amendment authority violation: {path}:{flag}")
        amendments[path] = row
    return amendments


def current_matches_expected_or_amended(
    repo_root: Path,
    relative_path: str,
    expected: str,
    amendments: dict[str, dict[str, Any]] | None = None,
) -> bool:
    path = repo_root / relative_path
    if matches_expected_digest(path, expected):
        return True
    records = amendments if amendments is not None else load_verified_lcm16a_amendments(repo_root)
    row = records.get(relative_path)
    if not row or row.get("previous_sha256") != _normalise_expected(expected):
        return False
    return matches_expected_digest(path, row["amended_sha256"])
