from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from jsonschema import Draft202012Validator

RELEASE_ROOT = PurePosixPath("releases/unified_consolidation/uc04/w1b")
INDEX_RELATIVE = RELEASE_ROOT / "PATCH_FILE_INDEX.txt"
LEDGER_RELATIVE = RELEASE_ROOT / "PATCH_FILE_HASHES.sha256"
MANIFEST_RELATIVE = RELEASE_ROOT / "PATCH_MANIFEST.json"
QA_RELATIVE = RELEASE_ROOT / "QA_REPORT.json"

CRLF_SUFFIXES = {".ps1", ".bat", ".cmd"}
LF_SUFFIXES = {
    ".ini",
    ".json",
    ".md",
    ".mq5",
    ".mqh",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
DISALLOWED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "node_modules",
}
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1\n"
HIGH_CONFIDENCE_SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bsk-[A-Za-z0-9]{32,}\b"),
)
LEDGER_ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>.+)$")
POWERSHELL_SCOPED_VARIABLES = {"env", "global", "local", "private", "script", "using", "variable", "function"}
POWERSHELL_COLON_INTERPOLATION = re.compile(r"\$(?P<name>[A-Za-z_][A-Za-z0-9_]*):")


class PackageValidationError(ValueError):
    """Raised when a release tree or ZIP violates the patch contract."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _validate_relative_path(raw: str) -> str:
    if not raw or raw != raw.strip():
        raise PackageValidationError(f"invalid blank or padded path: {raw!r}")
    if "\\" in raw:
        raise PackageValidationError(f"backslash is forbidden in patch index paths: {raw}")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise PackageValidationError(f"absolute path is forbidden: {raw}")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise PackageValidationError(f"unsafe relative path: {raw}")
    for part in path.parts:
        if part in DISALLOWED_PARTS:
            raise PackageValidationError(f"disallowed patch path segment {part!r}: {raw}")
        if part.endswith(" ") or part.endswith(".") or ":" in part:
            raise PackageValidationError(f"Windows-unsafe path segment {part!r}: {raw}")
        base = part.split(".", 1)[0].upper()
        if base in WINDOWS_RESERVED_NAMES:
            raise PackageValidationError(f"Windows-reserved path segment {part!r}: {raw}")
    return path.as_posix()


def _decode_utf8(relative: str, payload: bytes) -> str:
    if payload.startswith(b"\xef\xbb\xbf"):
        raise PackageValidationError(f"UTF-8 BOM is forbidden in patch text file: {relative}")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PackageValidationError(f"patch text file is not UTF-8: {relative}: {exc}") from exc


def _validate_content(relative: str, payload: bytes) -> None:
    if payload.startswith(LFS_POINTER_PREFIX):
        raise PackageValidationError(f"Git LFS pointer is forbidden in patch payload: {relative}")
    for pattern in HIGH_CONFIDENCE_SECRET_PATTERNS:
        if pattern.search(payload):
            raise PackageValidationError(f"high-confidence secret material detected: {relative}")

    suffix = PurePosixPath(relative).suffix.lower()
    if suffix in CRLF_SUFFIXES:
        decoded = _decode_utf8(relative, payload)
        for match in POWERSHELL_COLON_INTERPOLATION.finditer(decoded):
            if match.group("name").lower() not in POWERSHELL_SCOPED_VARIABLES:
                raise PackageValidationError(
                    f"PowerShell variable immediately followed by ':' must use braces or formatting: "
                    f"{relative}: {match.group(0)}"
                )
        if not payload.endswith(b"\r\n"):
            raise PackageValidationError(f"PowerShell/command file must end with CRLF: {relative}")
        if payload.replace(b"\r\n", b"").find(b"\n") != -1:
            raise PackageValidationError(f"bare LF found in CRLF-governed file: {relative}")
    elif suffix in LF_SUFFIXES:
        _decode_utf8(relative, payload)
        if b"\r\n" in payload or b"\r" in payload:
            raise PackageValidationError(f"CRLF/CR found in LF-governed file: {relative}")
        if payload and not payload.endswith(b"\n"):
            raise PackageValidationError(f"text file must end with LF: {relative}")


def _load_json_bytes(relative: str, payload: bytes) -> dict[str, Any]:
    text = _decode_utf8(relative, payload)
    value = json.loads(text)
    if not isinstance(value, dict):
        raise PackageValidationError(f"JSON root must be an object: {relative}")
    return value


def _parse_index(payload: bytes) -> list[str]:
    text = _decode_utf8(INDEX_RELATIVE.as_posix(), payload)
    if "\r" in text:
        raise PackageValidationError("PATCH_FILE_INDEX.txt must use LF line endings")
    rows = [_validate_relative_path(line) for line in text.splitlines() if line]
    if not rows:
        raise PackageValidationError("PATCH_FILE_INDEX.txt is empty")
    if rows != sorted(rows):
        raise PackageValidationError("PATCH_FILE_INDEX.txt must be ordinally sorted")
    if len(rows) != len(set(rows)):
        raise PackageValidationError("PATCH_FILE_INDEX.txt contains duplicate paths")
    folded = [row.casefold() for row in rows]
    if len(folded) != len(set(folded)):
        raise PackageValidationError("PATCH_FILE_INDEX.txt contains Windows case-colliding paths")
    required = {
        INDEX_RELATIVE.as_posix(),
        LEDGER_RELATIVE.as_posix(),
        MANIFEST_RELATIVE.as_posix(),
        QA_RELATIVE.as_posix(),
        (RELEASE_ROOT / "README.md").as_posix(),
        (RELEASE_ROOT / "INSTALL.md").as_posix(),
        (RELEASE_ROOT / "ROLLBACK.md").as_posix(),
        (RELEASE_ROOT / "COMMIT_MESSAGE.txt").as_posix(),
    }
    missing = sorted(required - set(rows))
    if missing:
        raise PackageValidationError(f"patch index is missing required release files: {missing}")
    return rows


def _parse_ledger(payload: bytes) -> dict[str, str]:
    text = _decode_utf8(LEDGER_RELATIVE.as_posix(), payload)
    if "\r" in text:
        raise PackageValidationError("PATCH_FILE_HASHES.sha256 must use LF line endings")
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line:
            continue
        match = LEDGER_ROW.fullmatch(line)
        if not match:
            raise PackageValidationError(f"invalid hash ledger row: {line!r}")
        relative = _validate_relative_path(match.group("path"))
        if relative in rows:
            raise PackageValidationError(f"duplicate hash ledger path: {relative}")
        rows[relative] = match.group("digest")
    return rows


def _resolve_schema_path(root: Path, document_path: Path, document: dict[str, Any]) -> Path:
    reference = document.get("$schema")
    if not isinstance(reference, str) or not reference:
        raise PackageValidationError(f"missing $schema in {document_path.relative_to(root).as_posix()}")
    schema_path = (document_path.parent / reference).resolve()
    root_resolved = root.resolve()
    try:
        schema_path.relative_to(root_resolved)
    except ValueError as exc:
        raise PackageValidationError(f"schema path escapes repository root: {reference}") from exc
    if not schema_path.is_file():
        raise PackageValidationError(f"referenced schema is missing: {schema_path}")
    return schema_path


def _validate_json_schema(root: Path, document_path: Path) -> None:
    document = _load_json_bytes(document_path.relative_to(root).as_posix(), document_path.read_bytes())
    schema_path = _resolve_schema_path(root, document_path, document)
    schema = _load_json_bytes(schema_path.relative_to(root).as_posix(), schema_path.read_bytes())
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # pragma: no cover - library formats the exact issue
        raise PackageValidationError(f"invalid JSON schema {schema_path}: {exc}") from exc
    issues = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path))
    if issues:
        issue = issues[0]
        location = "/".join(str(part) for part in issue.path) or "<root>"
        raise PackageValidationError(
            f"schema violation in {document_path.relative_to(root).as_posix()} at {location}: {issue.message}"
        )


def _tree_payloads(root: Path, paths: Iterable[str]) -> dict[str, bytes]:
    payloads: dict[str, bytes] = {}
    for relative in paths:
        target = root / PurePosixPath(relative)
        if target.is_symlink():
            raise PackageValidationError(f"symlink is forbidden in patch payload: {relative}")
        if not target.is_file():
            raise PackageValidationError(f"indexed patch file is missing: {relative}")
        payloads[relative] = target.read_bytes()
    return payloads


def _validate_contract(payloads: dict[str, bytes], *, root: Path | None = None) -> dict[str, Any]:
    index_payload = payloads.get(INDEX_RELATIVE.as_posix())
    ledger_payload = payloads.get(LEDGER_RELATIVE.as_posix())
    manifest_payload = payloads.get(MANIFEST_RELATIVE.as_posix())
    qa_payload = payloads.get(QA_RELATIVE.as_posix())
    if None in (index_payload, ledger_payload, manifest_payload, qa_payload):
        raise PackageValidationError("release control files are missing from payload")

    index = _parse_index(index_payload or b"")
    if set(payloads) != set(index):
        missing = sorted(set(index) - set(payloads))
        extra = sorted(set(payloads) - set(index))
        raise PackageValidationError(f"payload/index membership mismatch; missing={missing}, extra={extra}")

    ledger = _parse_ledger(ledger_payload or b"")
    expected_ledger = set(index) - {LEDGER_RELATIVE.as_posix()}
    if set(ledger) != expected_ledger:
        missing = sorted(expected_ledger - set(ledger))
        extra = sorted(set(ledger) - expected_ledger)
        raise PackageValidationError(f"hash ledger membership mismatch; missing={missing}, extra={extra}")

    for relative in index:
        payload = payloads[relative]
        _validate_content(relative, payload)
        if relative != LEDGER_RELATIVE.as_posix():
            actual = sha256_bytes(payload)
            if ledger[relative] != actual:
                raise PackageValidationError(
                    f"SHA-256 mismatch for {relative}: expected {ledger[relative]}, actual {actual}"
                )

    manifest = _load_json_bytes(MANIFEST_RELATIVE.as_posix(), manifest_payload or b"")
    qa = _load_json_bytes(QA_RELATIVE.as_posix(), qa_payload or b"")
    if manifest.get("patch_file_count") != len(index):
        raise PackageValidationError("PATCH_MANIFEST.json patch_file_count mismatch")
    if manifest.get("hash_ledger_entry_count") != len(ledger):
        raise PackageValidationError("PATCH_MANIFEST.json hash_ledger_entry_count mismatch")
    governed_payload_bytes = sum(
        len(payloads[path])
        for path in index
        if path not in {MANIFEST_RELATIVE.as_posix(), LEDGER_RELATIVE.as_posix()}
    )
    if manifest.get("payload_total_bytes_excluding_manifest_and_hash_ledger") != governed_payload_bytes:
        raise PackageValidationError(
            "PATCH_MANIFEST.json payload_total_bytes_excluding_manifest_and_hash_ledger mismatch"
        )
    if manifest.get("lfs_pointer_count") != 0:
        raise PackageValidationError("PATCH_MANIFEST.json must declare zero LFS pointers")
    if manifest.get("secret_finding_count") != 0:
        raise PackageValidationError("PATCH_MANIFEST.json must declare zero secret findings")
    if manifest.get("stage_id") != "UC04-W1B-Q":
        raise PackageValidationError("unexpected stage_id in PATCH_MANIFEST.json")
    if qa.get("stage_id") != "UC04-W1B-Q":
        raise PackageValidationError("unexpected stage_id in QA_REPORT.json")

    if root is not None:
        _validate_json_schema(root, root / MANIFEST_RELATIVE)
        _validate_json_schema(root, root / QA_RELATIVE)

    return {
        "stage_id": manifest["stage_id"],
        "patch_file_count": len(index),
        "hash_ledger_entry_count": len(ledger),
        "payload_total_bytes": sum(len(payloads[path]) for path in index),
        "governed_payload_bytes": governed_payload_bytes,
        "lfs_pointer_count": 0,
        "secret_finding_count": 0,
        "line_endings": "PASS",
        "schema_validation": "PASS" if root is not None else "DEFERRED_TO_TREE_VALIDATION",
    }


def verify_tree(repo_root: Path, *, payload_only: bool = False) -> dict[str, Any]:
    root = repo_root.resolve()
    index_path = root / INDEX_RELATIVE
    if not index_path.is_file():
        raise PackageValidationError(f"patch index is missing: {index_path}")
    index = _parse_index(index_path.read_bytes())
    payloads = _tree_payloads(root, index)

    if payload_only:
        actual_files = {
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file() or path.is_symlink()
        }
        if actual_files != set(index):
            missing = sorted(set(index) - actual_files)
            extra = sorted(actual_files - set(index))
            bytecode_extra = [
                relative
                for relative in extra
                if "__pycache__" in PurePosixPath(relative).parts
                or PurePosixPath(relative).suffix.lower() in {".pyc", ".pyo"}
            ]
            hint = ""
            if bytecode_extra:
                hint = (
                    "; Python bytecode mutated the isolated staging tree; invoke Python with "
                    "-B and PYTHONDONTWRITEBYTECODE=1"
                )
            raise PackageValidationError(
                f"staging tree contains unexpected membership; missing={missing}, extra={extra}{hint}"
            )

    return _validate_contract(payloads, root=root)


def _zip_member_is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def verify_zip(zip_path: Path, *, expected_sha256: str | None = None) -> dict[str, Any]:
    archive = zip_path.resolve()
    if not archive.is_file():
        raise PackageValidationError(f"ZIP does not exist: {archive}")
    actual_zip_sha256 = sha256_file(archive)
    if expected_sha256:
        normalized = expected_sha256.lower().removeprefix("sha256:")
        if not re.fullmatch(r"[0-9a-f]{64}", normalized):
            raise PackageValidationError("expected ZIP SHA-256 is not 64 lowercase hexadecimal characters")
        if actual_zip_sha256 != normalized:
            raise PackageValidationError(
                f"ZIP SHA-256 mismatch: expected {normalized}, actual {actual_zip_sha256}"
            )

    with zipfile.ZipFile(archive, "r") as handle:
        infos = handle.infolist()
        names: list[str] = []
        payloads: dict[str, bytes] = {}
        total_uncompressed = 0
        for info in infos:
            if info.is_dir():
                raise PackageValidationError(f"directory entries are forbidden in deterministic patch ZIP: {info.filename}")
            relative = _validate_relative_path(info.filename)
            if _zip_member_is_symlink(info):
                raise PackageValidationError(f"symlink ZIP entry is forbidden: {relative}")
            names.append(relative)
            total_uncompressed += info.file_size
            payloads[relative] = handle.read(info)
        if len(names) != len(set(names)):
            raise PackageValidationError("ZIP contains duplicate member names")
        if len({name.casefold() for name in names}) != len(names):
            raise PackageValidationError("ZIP contains Windows case-colliding member names")
        result = _validate_contract(payloads)
        if result["payload_total_bytes"] != total_uncompressed:
            raise PackageValidationError("ZIP uncompressed byte count mismatch")

    result.update(
        {
            "zip_path": str(archive),
            "zip_sha256": actual_zip_sha256,
            "zip_member_count": len(payloads),
            "zip_structure": "PASS",
        }
    )
    return result


def build_deterministic_zip(repo_root: Path, output: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    verify_tree(root)
    index = _parse_index((root / INDEX_RELATIVE).read_bytes())
    destination = output.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    if temporary.exists():
        temporary.unlink()
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
            for relative in index:
                payload = (root / PurePosixPath(relative)).read_bytes()
                info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.flag_bits |= 0x800
                handle.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return verify_zip(destination)


def _print_result(result: dict[str, Any]) -> None:
    print(json.dumps(result, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate or build the UC04-W1B-Q installable patch package.")
    sub = parser.add_subparsers(dest="command", required=True)

    tree = sub.add_parser("verify-tree")
    tree.add_argument("--repo-root", default=".")
    tree.add_argument("--payload-only", action="store_true")

    archive = sub.add_parser("verify-zip")
    archive.add_argument("--zip", required=True)
    archive.add_argument("--expected-sha256", default="")

    build = sub.add_parser("build-zip")
    build.add_argument("--repo-root", default=".")
    build.add_argument("--output", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "verify-tree":
            _print_result(verify_tree(Path(args.repo_root), payload_only=args.payload_only))
        elif args.command == "verify-zip":
            _print_result(verify_zip(Path(args.zip), expected_sha256=args.expected_sha256 or None))
        elif args.command == "build-zip":
            _print_result(build_deterministic_zip(Path(args.repo_root), Path(args.output)))
        else:  # pragma: no cover
            raise AssertionError(args.command)
    except PackageValidationError as exc:
        print(f"UC04-W1B-Q package validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
