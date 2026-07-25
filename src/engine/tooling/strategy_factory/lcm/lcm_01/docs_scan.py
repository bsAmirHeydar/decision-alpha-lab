from __future__ import annotations

import posixpath
import re
import urllib.parse
from pathlib import Path

MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
WIKI_LINK = re.compile(r"!?(?:\[\[)([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MAX_REPORTED_CANDIDATES = 6
_URI = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")


def _has_suffix(raw: str) -> bool:
    name = raw.rsplit("/", 1)[-1]
    return "." in name and not name.endswith(".")


def _normalize(candidate: str) -> tuple[str, bool]:
    candidate = candidate.replace("\\", "/")
    absolute = candidate.startswith("/")
    parts: list[str] = []
    escaped = False
    for part in candidate.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                escaped = True
                break
            parts.pop()
        else:
            parts.append(part)
    if absolute:
        # Repository links are interpreted root-relative after stripping the slash.
        escaped = False
    return "/".join(parts), escaped


def _resolve(
    source: str,
    source_parent: str,
    raw: str,
    known: set[str],
    stem_map: dict[str, list[str]],
) -> tuple[str, str, list[str], int]:
    raw = urllib.parse.unquote(raw.strip()).split("#", 1)[0].split("?", 1)[0]
    if not raw:
        return "ANCHOR_ONLY", "", [], 0
    if _URI.match(raw) or raw.startswith(("mailto:", "obsidian:")):
        return "EXTERNAL_URI", "", [], 0
    raw = raw.replace("\\", "/")
    root_relative = raw.lstrip("/")
    direct_raw = [posixpath.join(source_parent, raw) if source_parent else raw, root_relative]
    if not _has_suffix(raw):
        direct_raw.extend(
            [
                posixpath.join(source_parent, raw + ".md") if source_parent else raw + ".md",
                root_relative + ".md",
            ]
        )
    normalized: list[str] = []
    escaped_candidates: list[str] = []
    for candidate in direct_raw:
        value, escaped = _normalize(candidate)
        if escaped:
            escaped_candidates.append(candidate)
            continue
        if value not in normalized:
            normalized.append(value)
    hits = [candidate for candidate in normalized if candidate in known]
    if len(hits) == 1:
        return "RESOLVED_INTERNAL", hits[0], normalized[:MAX_REPORTED_CANDIDATES], len(normalized)
    if len(hits) > 1:
        return "AMBIGUOUS_INTERNAL", "", hits[:MAX_REPORTED_CANDIDATES], len(hits)

    if not _has_suffix(raw):
        stem = raw.rsplit("/", 1)[-1].casefold()
        stem_hits = stem_map.get(stem, [])
        if len(stem_hits) == 1:
            return "RESOLVED_INTERNAL", stem_hits[0], stem_hits, 1
        if len(stem_hits) > 1:
            return (
                "AMBIGUOUS_INTERNAL",
                "",
                stem_hits[:MAX_REPORTED_CANDIDATES],
                len(stem_hits),
            )
    if not normalized and escaped_candidates:
        return (
            "PATH_ESCAPE",
            "",
            escaped_candidates[:MAX_REPORTED_CANDIDATES],
            len(escaped_candidates),
        )
    return "UNRESOLVED", "", normalized[:MAX_REPORTED_CANDIDATES], len(normalized)


def scan(
    repo_root: Path,
    paths: list[str],
    known: set[str],
    limit_per_file: int,
) -> tuple[list[dict], list[dict]]:
    stem_map: dict[str, list[str]] = {}
    for path in paths:
        name = path.rsplit("/", 1)[-1]
        stem = name.rsplit(".", 1)[0].casefold()
        stem_map.setdefault(stem, []).append(path)
    for values in stem_map.values():
        values.sort()

    edges: list[dict] = []
    truncations: list[dict] = []
    patterns = ((MD_LINK, "MARKDOWN_LINK"), (WIKI_LINK, "OBSIDIAN_WIKILINK"))
    for source in paths:
        retained: list[dict] = []
        observed = 0
        source_parent = source.rpartition("/")[0]
        with (repo_root / source).open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, 1):
                for pattern, edge_type in patterns:
                    for match in pattern.finditer(line):
                        observed += 1
                        if len(retained) >= limit_per_file:
                            continue
                        raw = match.group(1).strip()
                        status, resolved, candidates, candidate_count = _resolve(
                            source, source_parent, raw, known, stem_map
                        )
                        retained.append(
                            {
                                "source_path": source,
                                "edge_type": edge_type,
                                "raw_target": raw,
                                "line_number": line_number,
                                "resolution_status": status,
                                "resolved_path": resolved,
                                "resolution_candidates": candidates,
                                "resolution_candidate_count": candidate_count,
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
            row["edge_type"],
            row["raw_target"],
        )
    )
    return edges, truncations
