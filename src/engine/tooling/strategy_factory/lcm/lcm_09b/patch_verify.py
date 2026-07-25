from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from .canonical import file_digest
from .errors import IntegrityError

_LEDGER_LINE = re.compile(r"^(sha256:[0-9a-f]{64})  ([^\r\n]+)$")


def _safe_relative_path(raw: str) -> str:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise IntegrityError(f"LCM09B_HASH_LEDGER_PATH_INVALID:{raw}")
    return path.as_posix()


def verify_hash_ledger(repo_root: Path, ledger_path: Path) -> dict:
    repo_root = repo_root.resolve()
    ledger_path = ledger_path.resolve()
    if not ledger_path.is_file():
        raise IntegrityError(f"LCM09B_HASH_LEDGER_MISSING:{ledger_path}")

    rows: list[tuple[str, str]] = []
    for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        match = _LEDGER_LINE.fullmatch(line)
        if match is None:
            raise IntegrityError(f"LCM09B_HASH_LEDGER_LINE_INVALID:{line_number}")
        expected, raw_path = match.groups()
        rows.append((expected, _safe_relative_path(raw_path)))

    if not rows:
        raise IntegrityError("LCM09B_HASH_LEDGER_EMPTY")
    paths = [path for _, path in rows]
    if len(paths) != len(set(paths)):
        raise IntegrityError("LCM09B_HASH_LEDGER_DUPLICATE_PATH")
    if paths != sorted(paths):
        raise IntegrityError("LCM09B_HASH_LEDGER_NOT_SORTED")

    mismatches: list[dict[str, str]] = []
    total_bytes = 0
    for expected, relative in rows:
        path = repo_root / relative
        if not path.is_file():
            mismatches.append({"path": relative, "reason": "MISSING"})
            continue
        total_bytes += path.stat().st_size
        actual = file_digest(path)
        if actual != expected:
            mismatches.append({"path": relative, "reason": "DIGEST_MISMATCH", "expected": expected, "actual": actual})

    if mismatches:
        raise IntegrityError(f"LCM09B_HASH_LEDGER_VERIFICATION_FAILED:{mismatches[:10]}")
    return {
        "passed": True,
        "verified_file_count": len(rows),
        "verified_byte_count": total_bytes,
        "ledger_path": ledger_path.as_posix(),
    }
