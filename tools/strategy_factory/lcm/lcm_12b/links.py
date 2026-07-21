from __future__ import annotations

import posixpath
import re
from collections import defaultdict
from pathlib import PurePosixPath
from urllib.parse import unquote

_MD = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
_WIKI = re.compile(r"(!?\[\[)([^\]]+)(\]\])")
_EXTERNAL = ("http://", "https://", "mailto:", "data:", "obsidian:")


def normalize_path(path: str) -> str:
    path = path.replace("\\", "/")
    parts: list[str] = []
    for part in PurePosixPath(path).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return "/".join(parts)


def split_target(raw: str):
    value = raw.strip().strip("<>")
    title = ""
    if " " in value and not value.startswith(("./", "../")):
        first, rest = value.split(" ", 1)
        if "." in PurePosixPath(first).name:
            value = first
            title = " " + rest
    anchor = ""
    if "#" in value:
        value, anchor = value.split("#", 1)
        anchor = "#" + anchor
    return value, anchor, title


def resolve_markdown(source_path: str, raw: str, existing_paths: set[str]):
    value, anchor, title = split_target(raw)
    if not value or value.startswith(_EXTERNAL) or value.startswith("#"):
        return None, anchor, title
    value = unquote(value).replace("\\", "/")
    if value.startswith("/"):
        candidate = normalize_path(value.lstrip("/"))
    elif value in existing_paths:
        candidate = value
    elif value.startswith(("docs/", "lab/", "registry/", "mql5/", "tools/")):
        candidate = normalize_path(value)
    else:
        candidate = normalize_path(posixpath.join(posixpath.dirname(source_path), value))
    if candidate in existing_paths:
        return candidate, anchor, title
    if not PurePosixPath(candidate).suffix:
        for suffix in (".md", ".mdx", ".rst", ".txt", ".adoc"):
            if candidate + suffix in existing_paths:
                return candidate + suffix, anchor, title
    return candidate, anchor, title


def relative_reference(source_path: str, target_path: str) -> str:
    return posixpath.relpath(target_path, posixpath.dirname(source_path) or ".")


def build_basename_index(paths: set[str]):
    index: dict[str, list[str]] = defaultdict(list)
    for path in sorted(paths):
        index[PurePosixPath(path).stem.lower()].append(path)
    return dict(index)


def build_raw_move_pattern(move_map: dict[str, str]) -> re.Pattern[str] | None:
    """Compile one alternation for all legacy paths.

    A single regex pass replaces the former O(documents × move-count × bytes)
    loop while preserving longest-path-first matching semantics.
    """
    sources = sorted(move_map, key=lambda value: (-len(value), value))
    if not sources:
        return None
    return re.compile("|".join(re.escape(source) for source in sources))


def resolve_wiki(
    raw: str,
    source_path: str,
    existing_paths: set[str],
    basename_index: dict[str, list[str]],
):
    target = raw.split("|", 1)[0].strip()
    alias = raw[len(target) :]
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    target = target.replace("\\", "/")
    if not target:
        return None, anchor, alias
    candidate = normalize_path(target)
    candidates: list[str] = []
    if "/" in candidate:
        if candidate in existing_paths:
            candidates = [candidate]
        elif candidate + ".md" in existing_paths:
            candidates = [candidate + ".md"]
        else:
            relative = normalize_path(posixpath.join(posixpath.dirname(source_path), candidate))
            if relative in existing_paths:
                candidates = [relative]
            elif relative + ".md" in existing_paths:
                candidates = [relative + ".md"]
    else:
        candidates = basename_index.get(PurePosixPath(candidate).stem.lower(), [])
    if len(candidates) == 1:
        return candidates[0], anchor, alias
    return None, anchor, alias


def rewrite_document(
    text: str,
    old_source_path: str,
    new_source_path: str,
    move_map: dict[str, str],
    existing_before: set[str],
    existing_after: set[str],
    *,
    before_index: dict[str, list[str]] | None = None,
    raw_pattern: re.Pattern[str] | None = None,
):
    before_index = before_index or build_basename_index(existing_before)
    records: list[dict] = []

    def markdown_replace(match: re.Match[str]) -> str:
        raw = match.group(2)
        resolved, anchor, title = resolve_markdown(old_source_path, raw, existing_before)
        if not resolved or resolved not in move_map:
            return match.group(0)
        target = move_map[resolved]
        new_raw = relative_reference(new_source_path, target) + anchor + title
        records.append(
            {
                "kind": "MARKDOWN",
                "raw_before": raw,
                "raw_after": new_raw,
                "resolved_before": resolved,
                "resolved_after": target,
            }
        )
        return match.group(1) + new_raw + match.group(3)

    output = _MD.sub(markdown_replace, text)

    def wiki_replace(match: re.Match[str]) -> str:
        raw = match.group(2)
        resolved, anchor, alias = resolve_wiki(
            raw, old_source_path, existing_before, before_index
        )
        if not resolved or resolved not in move_map:
            return match.group(0)
        target = move_map[resolved]
        target_no_extension = (
            target.rsplit(".", 1)[0] if "." in PurePosixPath(target).name else target
        )
        new_raw = target_no_extension + anchor + alias
        records.append(
            {
                "kind": "WIKI",
                "raw_before": raw,
                "raw_after": new_raw,
                "resolved_before": resolved,
                "resolved_after": target,
            }
        )
        return match.group(1) + new_raw + match.group(3)

    output = _WIKI.sub(wiki_replace, output)

    pattern = raw_pattern if raw_pattern is not None else build_raw_move_pattern(move_map)
    raw_counts: dict[str, int] = defaultdict(int)

    if pattern is not None:
        def raw_replace(match: re.Match[str]) -> str:
            source = match.group(0)
            raw_counts[source] += 1
            return move_map[source]

        output = pattern.sub(raw_replace, output)

    for source in sorted(raw_counts):
        target = move_map[source]
        records.append(
            {
                "kind": "RAW_PATH",
                "raw_before": source,
                "raw_after": target,
                "resolved_before": source,
                "resolved_after": target,
                "occurrence_count": raw_counts[source],
            }
        )

    for record in records:
        record["destination_exists"] = record["resolved_after"] in existing_after
        record["validation_status"] = (
            "PASS" if record["destination_exists"] else "FAILED"
        )
    return output, records
