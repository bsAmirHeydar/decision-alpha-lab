#!/usr/bin/env python3
"""Safely add deterministic IDs to normative Obsidian notes.

The migration is intentionally narrow:
- never renames a file;
- never edits links, titles, tags, or note bodies;
- preserves existing IDs;
- inserts only missing IDs into existing YAML frontmatter;
- fails closed on duplicate/colliding IDs or malformed frontmatter;
- applies atomically and rolls back on write failure;
- emits exact changed-path and before/after hash evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

MIGRATION_ID = "AIEOS_OBSIDIAN_NOTE_ID_NORMALIZATION_V1"
ID_PREFIX = "AIEOS-"
SKIP_FRONTMATTER = {
    "README.md",
    "README_FA.md",
    "AGENTS.md",
    "MASTER_PLAYBOOK.md",
    "INSTALLATION.md",
    "CHANGELOG.md",
}


@dataclass(frozen=True)
class PlannedChange:
    path: str
    note_id: str
    before_sha256: str
    after_sha256: str
    newline: str
    bom: bool
    change_kind: str = "INSERT_MISSING_ID_ONLY"


@dataclass(frozen=True)
class MigrationReport:
    schema_version: str
    migration_id: str
    vault_root: str
    note_count: int
    normative_note_count: int
    exempt_note_count: int
    existing_id_count_before: int
    resolved_id_count_after: int
    planned_change_count: int
    applied_change_count: int
    collision_count: int
    malformed_frontmatter_count: int
    idempotent_after_apply: bool
    backup_path: str | None
    backup_sha256: str | None
    changes: tuple[PlannedChange, ...]
    status: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def deterministic_note_id(relative_path: str) -> str:
    """Legacy helper retained for tests; production migration uses the canonical map."""
    normalized = relative_path.replace("\\", "/")
    suffix = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10].upper()
    return f"{ID_PREFIX}{suffix}"


def load_canonical_map(path: Path) -> tuple[dict[str, str], str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "1.0.0" or value.get("map_id") != "AIEOS_CANONICAL_NOTE_ID_MAP_V1":
        raise ValueError("invalid_canonical_map_identity")
    entries = value.get("entries")
    if not isinstance(entries, dict) or not entries:
        raise ValueError("invalid_canonical_map_entries")
    material = dict(value)
    expected = material.pop("map_digest", None)
    actual = "sha256:" + hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
    if expected != actual:
        raise ValueError("canonical_map_digest_mismatch")
    normalized = {str(k).replace("\\", "/"): str(v) for k, v in entries.items()}
    if len(set(normalized.values())) != len(normalized):
        raise ValueError("canonical_map_duplicate_ids")
    if int(value.get("normative_note_count", -1)) != len(normalized):
        raise ValueError("canonical_map_count_mismatch")
    return normalized, actual


def _decode(raw: bytes) -> tuple[str, bool, str]:
    bom = raw.startswith(b"\xef\xbb\xbf")
    payload = raw[3:] if bom else raw
    text = payload.decode("utf-8")
    newline = "\r\n" if b"\r\n" in payload else "\n"
    return text, bom, newline


def _encode(text: str, bom: bool) -> bytes:
    data = text.encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if bom else data


def _frontmatter_bounds(text: str, newline: str) -> tuple[int, int]:
    opening = f"---{newline}"
    if not text.startswith(opening):
        raise ValueError("missing_or_invalid_frontmatter")
    closing = f"{newline}---{newline}"
    end = text.find(closing, len(opening))
    if end < 0:
        raise ValueError("unterminated_frontmatter")
    return len(opening), end


def _extract_id(frontmatter: str) -> str | None:
    found: list[str] = []
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if stripped.startswith("id:"):
            value = stripped[3:].strip().strip('"').strip("'")
            if value:
                found.append(value)
    if len(found) > 1:
        raise ValueError("multiple_id_fields")
    return found[0] if found else None


def _insert_id(raw: bytes, note_id: str) -> bytes:
    text, bom, newline = _decode(raw)
    start, _ = _frontmatter_bounds(text, newline)
    updated = text[:start] + f"id: {note_id}{newline}" + text[start:]
    # Safety proof: removing exactly the inserted line recreates the original bytes.
    candidate = updated[:start] + updated[start + len(f"id: {note_id}{newline}"):]
    if candidate != text:
        raise AssertionError("insert_only_invariant_failed")
    return _encode(updated, bom)


def _iter_notes(vault: Path) -> tuple[Path, ...]:
    return tuple(sorted(path for path in vault.rglob("*.md") if path.is_file()))


def plan(vault: Path, canonical_map: dict[str, str] | None = None) -> tuple[tuple[PlannedChange, ...], dict[Path, bytes], dict[Path, bytes], dict[str, str], list[str], list[str]]:
    notes = _iter_notes(vault)
    existing_by_id: dict[str, str] = {}
    originals: dict[Path, bytes] = {}
    updated: dict[Path, bytes] = {}
    changes: list[PlannedChange] = []
    collisions: list[str] = []
    malformed: list[str] = []

    normative_paths = {path.relative_to(vault).as_posix() for path in notes if path.name not in SKIP_FRONTMATTER}
    if canonical_map is not None:
        unknown_paths = sorted(normative_paths - set(canonical_map))
        missing_paths = sorted(set(canonical_map) - normative_paths)
        malformed.extend(f"unknown_normative_path:{item}" for item in unknown_paths)
        malformed.extend(f"canonical_path_missing_from_vault:{item}" for item in missing_paths)
        if unknown_paths or missing_paths:
            return (), originals, {}, existing_by_id, collisions, malformed

    # Pass 1: inspect existing IDs and reject duplicate identity before planning changes.
    for path in notes:
        rel = path.relative_to(vault).as_posix()
        raw = path.read_bytes()
        originals[path] = raw
        if path.name in SKIP_FRONTMATTER:
            continue
        try:
            text, _, newline = _decode(raw)
            start, end = _frontmatter_bounds(text, newline)
            note_id = _extract_id(text[start:end])
        except (UnicodeDecodeError, ValueError) as exc:
            malformed.append(f"{rel}:{exc}")
            continue
        if note_id:
            if canonical_map is not None and canonical_map.get(rel) != note_id:
                malformed.append(f"existing_id_mismatch:{rel}:{note_id}:{canonical_map.get(rel)}")
            elif note_id in existing_by_id:
                collisions.append(f"duplicate_existing_id:{note_id}:{existing_by_id[note_id]}:{rel}")
            else:
                existing_by_id[note_id] = rel

    if malformed or collisions:
        return (), originals, {}, existing_by_id, collisions, malformed

    # Pass 2: plan deterministic additions and check future collisions.
    future_ids = dict(existing_by_id)
    for path in notes:
        if path.name in SKIP_FRONTMATTER:
            continue
        rel = path.relative_to(vault).as_posix()
        raw = originals[path]
        text, bom, newline = _decode(raw)
        start, end = _frontmatter_bounds(text, newline)
        existing = _extract_id(text[start:end])
        if existing:
            continue
        note_id = canonical_map[rel] if canonical_map is not None else deterministic_note_id(rel)
        prior = future_ids.get(note_id)
        if prior is not None and prior != rel:
            collisions.append(f"deterministic_id_collision:{note_id}:{prior}:{rel}")
            continue
        future_ids[note_id] = rel
        new_raw = _insert_id(raw, note_id)
        updated[path] = new_raw
        changes.append(
            PlannedChange(
                path=f"docs/history/aieos_legacy/{rel}",
                note_id=note_id,
                before_sha256=_sha256(raw),
                after_sha256=_sha256(new_raw),
                newline="CRLF" if newline == "\r\n" else "LF",
                bom=bom,
            )
        )
    return tuple(changes), originals, updated, future_ids, collisions, malformed


def _backup(vault: Path, paths: Iterable[Path], destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(paths):
            rel = path.relative_to(vault).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(2026, 7, 22, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return _sha256(destination.read_bytes())


def _atomic_write(path: Path, data: bytes) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def apply_transactionally(updated: dict[Path, bytes], originals: dict[Path, bytes]) -> None:
    written: list[Path] = []
    try:
        for path in sorted(updated):
            _atomic_write(path, updated[path])
            written.append(path)
    except Exception:
        for path in reversed(written):
            _atomic_write(path, originals[path])
        raise


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--vault", default="docs/history/aieos_legacy")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-zip")
    parser.add_argument("--report", required=True)
    parser.add_argument("--runtime-index", required=True)
    parser.add_argument("--expect-note-count", type=int)
    parser.add_argument("--canonical-map", default="tools/engineering/obsidian_identity/canonical_note_id_map.v1.json")
    args = parser.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    vault = (repo / args.vault).resolve()
    if not vault.is_dir() or repo not in vault.parents:
        print("ERROR: invalid vault path", file=sys.stderr)
        return 2

    notes = _iter_notes(vault)
    if args.expect_note_count is not None and len(notes) != args.expect_note_count:
        print(f"ERROR: expected {args.expect_note_count} notes, found {len(notes)}", file=sys.stderr)
        return 2

    try:
        canonical_map, canonical_map_digest = load_canonical_map((repo / args.canonical_map).resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: canonical map validation failed: {exc}", file=sys.stderr)
        return 2

    changes, originals, updated, existing, collisions, malformed = plan(vault, canonical_map)
    normative_count = sum(path.name not in SKIP_FRONTMATTER for path in notes)
    exempt_count = len(notes) - normative_count
    backup_path: str | None = None
    backup_hash: str | None = None
    applied = 0
    idempotent = False
    status = "PLANNED"

    if collisions or malformed:
        status = "BLOCKED"
    elif args.apply:
        if changes and not args.backup_zip:
            print("ERROR: --backup-zip is required with --apply", file=sys.stderr)
            return 2
        if changes:
            backup = Path(args.backup_zip).resolve()
            backup_hash = _backup(vault, updated.keys(), backup)
            backup_path = backup.name
            apply_transactionally(updated, originals)
            applied = len(changes)
        second_changes, *_rest = plan(vault, canonical_map)
        idempotent = len(second_changes) == 0
        status = "PASS" if idempotent else "FAILED_IDEMPOTENCY"
    else:
        idempotent = len(changes) == 0

    report = MigrationReport(
        schema_version="1.0.0",
        migration_id=MIGRATION_ID,
        vault_root=args.vault.replace("\\", "/"),
        note_count=len(notes),
        normative_note_count=normative_count,
        exempt_note_count=exempt_count,
        existing_id_count_before=max(0, len(existing) - len(changes)),
        resolved_id_count_after=len(existing),
        planned_change_count=len(changes),
        applied_change_count=applied,
        collision_count=len(collisions),
        malformed_frontmatter_count=len(malformed),
        idempotent_after_apply=idempotent,
        backup_path=backup_path,
        backup_sha256=backup_hash,
        changes=changes,
        status=status,
    )
    report_dict = asdict(report)
    report_dict["canonical_map_digest"] = canonical_map_digest
    report_dict["collisions"] = collisions
    report_dict["malformed_frontmatter"] = malformed
    report_dict["report_digest"] = _sha256(json.dumps(report_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    write_json((repo / args.report).resolve(), report_dict)

    runtime_paths = [change.path for change in changes]
    runtime_paths.extend([args.report.replace("\\", "/"), args.runtime_index.replace("\\", "/")])
    index_path = (repo / args.runtime_index).resolve()
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(sorted(set(runtime_paths))) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({
        "status": status,
        "notes": len(notes),
        "normative_notes": normative_count,
        "existing_ids_before": max(0, len(existing) - len(changes)),
        "resolved_ids_after": len(existing),
        "planned_changes": len(changes),
        "applied_changes": applied,
        "idempotent": idempotent,
        "collisions": len(collisions),
        "malformed": len(malformed),
    }, sort_keys=True))
    return 0 if status in {"PLANNED", "PASS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
