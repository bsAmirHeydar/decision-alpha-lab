from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

import yaml

PATH_EXTENSIONS = (
    ".json", ".yaml", ".yml", ".md", ".py", ".mq5", ".mqh", ".csv",
    ".txt", ".set", ".onnx", ".ps1", ".jsonl", ".toml", ".ini"
)
QUOTED_STRING = re.compile(r"[\"']([^\"'\r\n]{1,512})[\"']")


def _walk_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield key
            yield from _walk_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _walk_strings(item)


def _looks_like_path(value: str) -> bool:
    stripped = value.strip()
    if not stripped or len(stripped) > 1024:
        return False
    normalized = stripped.replace("\\", "/").split("#", 1)[0].split("?", 1)[0]
    return "/" in normalized and normalized.lower().endswith(PATH_EXTENSIONS)


def _structured_strings(path: Path, extension: str) -> Iterator[tuple[int, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        if extension == ".json":
            value = json.loads(text)
            for item in _walk_strings(value):
                yield 0, item
            return
        if extension == ".jsonl":
            for line_number, line in enumerate(text.splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for item in _walk_strings(value):
                    yield line_number, item
            return
        if extension in {".yaml", ".yml"}:
            value = yaml.safe_load(text)
            for item in _walk_strings(value):
                yield 0, item
            return
        if extension == ".toml":
            value = tomllib.loads(text)
            for item in _walk_strings(value):
                yield 0, item
            return
    except Exception:
        pass
    for line_number, line in enumerate(text.splitlines(), 1):
        if "/" not in line and "\\" not in line:
            continue
        for match in QUOTED_STRING.finditer(line):
            yield line_number, match.group(1)


def scan(
    repo_root: Path,
    paths: list[str],
    known: set[str],
    limit_per_file: int,
) -> tuple[list[dict], list[dict]]:
    edges: list[dict] = []
    truncations: list[dict] = []
    for source in paths:
        retained: list[dict] = []
        observed = 0
        extension = PurePosixPath(source).suffix.lower()
        seen: set[tuple[int, str]] = set()
        for line_number, candidate in _structured_strings(repo_root / source, extension):
            if not _looks_like_path(candidate):
                continue
            raw = candidate.strip().replace("\\", "/").split("#", 1)[0].split("?", 1)[0]
            key = (line_number, raw)
            if key in seen:
                continue
            seen.add(key)
            observed += 1
            if len(retained) >= limit_per_file:
                continue
            candidates = [
                raw.lstrip("/"),
                (PurePosixPath(source).parent / PurePosixPath(raw)).as_posix(),
            ]
            candidates = list(dict.fromkeys(candidates))
            hits = [candidate for candidate in candidates if candidate in known]
            status = (
                "RESOLVED_INTERNAL"
                if len(hits) == 1
                else "AMBIGUOUS_INTERNAL"
                if len(hits) > 1
                else "UNRESOLVED"
            )
            retained.append(
                {
                    "source_path": source,
                    "edge_type": "CONFIG_PATH_REFERENCE",
                    "raw_target": raw,
                    "line_number": line_number,
                    "resolution_status": status,
                    "resolved_path": hits[0] if len(hits) == 1 else "",
                    "resolution_candidates": candidates,
                    "semantic_reachability_claimed": False,
                }
            )
        if observed > limit_per_file:
            truncations.append(
                {
                    "path": source,
                    "observed_edge_count": observed,
                    "retained_edge_count": limit_per_file,
                    "reason": "PER_FILE_EDGE_SAFETY_LIMIT",
                }
            )
        edges.extend(retained)
    edges.sort(
        key=lambda row: (
            row["source_path"],
            row["line_number"],
            row["raw_target"],
        )
    )
    return edges, truncations
