"""External source-archive creation and exact recovery drill."""
from __future__ import annotations

import hashlib
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

from .io_utils import iter_jsonl_gz, sha256_file

_FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def create_source_archive(repo_root: Path, artifact_inventory_path: Path, output_path: Path, *, overwrite: bool = False) -> dict:
    rows = list(iter_jsonl_gz(artifact_inventory_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and not overwrite:
        status = "reused_existing"
    else:
        if output_path.exists():
            output_path.unlink()
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
            for row in rows:
                rel = row["path"]
                source = repo_root / rel
                info = zipfile.ZipInfo(rel, date_time=_FIXED_ZIP_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100644 & 0xFFFF) << 16
                if source.is_symlink():
                    data = source.readlink().as_posix().encode("utf-8")
                else:
                    data = source.read_bytes()
                archive.writestr(info, data)
        status = "created"
    return {
        "status": "PASS",
        "archive_status": status,
        "archive_path": str(output_path.resolve()),
        "archive_size": output_path.stat().st_size,
        "archive_sha256": sha256_file(output_path),
        "file_count": len(rows),
    }


def root_digest_from_rows(rows: Iterable[dict]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda x: x["path"]):
        digest.update(f"{row['sha256']} {row['size']} {row['path']}\n".encode("utf-8"))
    return digest.hexdigest()


def recovery_drill(artifact_inventory_path: Path, archive_path: Path) -> dict:
    expected_rows = list(iter_jsonl_gz(artifact_inventory_path))
    expected = {row["path"]: row for row in expected_rows}
    with tempfile.TemporaryDirectory(prefix="alpha-lab-uc01-recovery-") as temp:
        temp_root = Path(temp)
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(temp_root)
        actual_rows = []
        missing = []
        mismatches = []
        for rel, row in sorted(expected.items()):
            path = temp_root / rel
            if not path.is_file():
                missing.append(rel)
                continue
            actual_hash = sha256_file(path)
            actual_size = path.stat().st_size
            actual_rows.append({"path": rel, "sha256": actual_hash, "size": actual_size})
            if actual_hash != row["sha256"] or actual_size != row["size"]:
                mismatches.append({
                    "path": rel,
                    "expected_sha256": row["sha256"],
                    "actual_sha256": actual_hash,
                    "expected_size": row["size"],
                    "actual_size": actual_size,
                })
        extra = sorted(
            path.relative_to(temp_root).as_posix()
            for path in temp_root.rglob("*")
            if path.is_file() and path.relative_to(temp_root).as_posix() not in expected
        )
        actual_digest = root_digest_from_rows(actual_rows)
        expected_digest = root_digest_from_rows(expected_rows)
    return {
        "status": "PASS" if not missing and not extra and not mismatches and actual_digest == expected_digest else "FAILED",
        "archive_path": str(archive_path.resolve()),
        "archive_sha256": sha256_file(archive_path),
        "expected_file_count": len(expected_rows),
        "restored_file_count": len(actual_rows),
        "missing_paths": missing[:100],
        "extra_paths": extra[:100],
        "mismatches": mismatches[:100],
        "expected_root_digest": expected_digest,
        "actual_root_digest": actual_digest,
        "workspace_destroyed_after_drill": True,
    }
