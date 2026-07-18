from __future__ import annotations

import hashlib
import io
import os
import stat
import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .canonical import digest_object, normalize_root_relative
from .scope import ScopePolicy, classify_path


@dataclass(frozen=True)
class ZipLayer:
    layer_id: str
    archive_path: Path
    strip_prefix: str = ""


@dataclass(frozen=True)
class VirtualSource:
    layer_id: str
    archive_path: Path
    member_name: str
    root_relative_path: str
    size_bytes: int
    mode_octal: str


def _to_root_relative(member_name: str, strip_prefix: str) -> str | None:
    name = member_name.replace("\\", "/")
    if name.endswith("/"):
        return None
    if strip_prefix:
        prefix = strip_prefix.rstrip("/") + "/"
        if not name.startswith(prefix):
            return None
        name = name[len(prefix):]
    if not name:
        return None
    return normalize_root_relative(name)


def build_virtual_index(layers: Iterable[ZipLayer], policy: ScopePolicy) -> tuple[dict[str, VirtualSource], list[dict]]:
    index: dict[str, VirtualSource] = {}
    exclusions: list[dict] = []
    for layer in layers:
        with zipfile.ZipFile(layer.archive_path) as archive:
            for info in archive.infolist():
                rel = _to_root_relative(info.filename, layer.strip_prefix)
                if rel is None:
                    continue
                included, reason = classify_path(rel, policy)
                if not included:
                    exclusions.append({"path": rel, "reason": reason, "layer_id": layer.layer_id})
                    index.pop(rel, None)
                    continue
                mode = (info.external_attr >> 16) & 0xFFFF
                index[rel] = VirtualSource(
                    layer_id=layer.layer_id,
                    archive_path=layer.archive_path,
                    member_name=info.filename,
                    root_relative_path=rel,
                    size_bytes=info.file_size,
                    mode_octal=format(stat.S_IMODE(mode) if mode else 0o644, "04o"),
                )
    return index, exclusions


def materialize_virtual_restore(
    layers: Iterable[ZipLayer],
    index: dict[str, VirtualSource],
    tar_path: Path,
) -> tuple[list[dict], dict]:
    """Restore the final overlay into a clean tar container and verify every member.

    The tar is a temporary restoration medium, not a deliverable. Every final path is
    written exactly once from its authoritative layer and then read back in a second
    pass for complete path/hash comparison.
    """
    layers = list(layers)
    if tar_path.exists():
        tar_path.unlink()
    records_by_path: dict[str, dict] = {}
    selected_by_layer: dict[str, dict[str, VirtualSource]] = {}
    for rel, source in index.items():
        selected_by_layer.setdefault(source.layer_id, {})[source.member_name] = source

    with tarfile.open(tar_path, mode="w") as restored:
        for layer in layers:
            selected = selected_by_layer.get(layer.layer_id, {})
            if not selected:
                continue
            with zipfile.ZipFile(layer.archive_path) as archive:
                for info in archive.infolist():
                    source = selected.get(info.filename)
                    if source is None:
                        continue
                    data = archive.read(info)
                    digest = "sha256:" + hashlib.sha256(data).hexdigest()
                    binary = b"\x00" in data[:8192]
                    ti = tarfile.TarInfo(source.root_relative_path)
                    ti.size = len(data)
                    ti.mode = int(source.mode_octal, 8)
                    ti.mtime = 0
                    restored.addfile(ti, io.BytesIO(data))
                    records_by_path[source.root_relative_path] = {
                        "path": source.root_relative_path,
                        "kind": "FILE",
                        "size_bytes": len(data),
                        "sha256": digest,
                        "symlink_target": None,
                        "mode_octal": source.mode_octal,
                        "extension": Path(source.root_relative_path).suffix.lower(),
                        "binary": binary,
                        "source_layer_id": source.layer_id,
                        "source_archive_sha256": "",
                        "source_member": source.member_name,
                    }

    layer_digests: dict[Path, str] = {}
    for layer in layers:
        h = hashlib.sha256()
        with layer.archive_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                h.update(chunk)
        layer_digests[layer.archive_path] = "sha256:" + h.hexdigest()
    for record in records_by_path.values():
        src = index[record["path"]]
        record["source_archive_sha256"] = layer_digests[src.archive_path]

    expected = records_by_path
    mismatches: list[dict] = []
    seen: set[str] = set()
    with tarfile.open(tar_path, mode="r") as restored:
        for member in restored:
            if not member.isfile():
                continue
            rel = normalize_root_relative(member.name)
            seen.add(rel)
            handle = restored.extractfile(member)
            if handle is None:
                mismatches.append({"path": rel, "reason": "RESTORED_MEMBER_UNREADABLE"})
                continue
            h = hashlib.sha256()
            size = 0
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                h.update(chunk)
            actual_digest = "sha256:" + h.hexdigest()
            source = expected.get(rel)
            if source is None:
                mismatches.append({"path": rel, "reason": "UNDECLARED_RESTORED_MEMBER"})
            elif source["size_bytes"] != size or source["sha256"] != actual_digest:
                mismatches.append({
                    "path": rel,
                    "reason": "RESTORED_CONTENT_MISMATCH",
                    "expected_size": source["size_bytes"],
                    "actual_size": size,
                    "expected_sha256": source["sha256"],
                    "actual_sha256": actual_digest,
                })
    missing = sorted(set(expected) - seen)
    mismatches.extend({"path": rel, "reason": "RESTORED_MEMBER_MISSING"} for rel in missing)
    records = [records_by_path[path] for path in sorted(records_by_path)]
    report = {
        "schema_version": "1.0.0",
        "method": "CLEAN_TAR_RESTORATION_CONTAINER_AND_FULL_PATH_HASH_COMPARISON",
        "source_layer_count": len(layers),
        "source_layers": [
            {
                "layer_id": layer.layer_id,
                "archive_name": layer.archive_path.name,
                "archive_sha256": layer_digests[layer.archive_path],
                "strip_prefix": layer.strip_prefix,
            }
            for layer in layers
        ],
        "copied_record_count": len(records),
        "verified_record_count": len(records) - len(mismatches),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "passed": not mismatches,
        "restoration_container_retained": False,
        "external_artifacts_restored": False,
        "git_metadata_restored": False,
        "claim_ceiling": "CONTENT_RESTORE_REHEARSAL_REFERENCE_ONLY",
        "restore_rehearsal_digest": "",
    }
    report["restore_rehearsal_digest"] = digest_object(report, "restore_rehearsal_digest")
    return records, report
