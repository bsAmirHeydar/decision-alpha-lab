"""Deterministic IO helpers for UC-02."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from typing import Iterable, Iterator


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_jsonl_gz(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        # mtime=0 makes gzip output deterministic.
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                zipped.write(payload.encode("utf-8") + b"\n")


def iter_jsonl_gz(path: Path) -> Iterator[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"JSONL row {number} is not an object: {path}")
            yield value


def root_digest(rows: Iterable[dict], *, key_fields: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    ordered = sorted(rows, key=lambda row: tuple(str(row.get(key, "")) for key in key_fields))
    for row in ordered:
        payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest.update(payload.encode("utf-8") + b"\n")
    return digest.hexdigest()
