"""Documentation, schema and path-reference inventory."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml

from .classification import owner_domain
from .constants import PATH_REFERENCE_PREFIXES, TEXT_SUFFIXES
from .io_utils import safe_read_text

_WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")
_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])((?:" + "|".join(re.escape(prefix) for prefix in PATH_REFERENCE_PREFIXES) + r")[A-Za-z0-9_./\\()\[\] -]{2,240})"
)
_ID_LINE_RE = re.compile(r"^id:\s*([^\s#]+)\s*$", re.MULTILINE)


def _frontmatter(text: str) -> tuple[dict, str, str | None]:
    if not text.startswith("---\n"):
        return {}, text, None
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text, "unterminated_frontmatter"
    try:
        data = yaml.safe_load(text[4:end]) or {}
        if not isinstance(data, dict):
            return {}, text[end + 5 :], "frontmatter_not_mapping"
        return data, text[end + 5 :], None
    except Exception as exc:
        return {}, text[end + 5 :], f"frontmatter_parse_error:{type(exc).__name__}"


def scan_documents(repo_root: Path, doc_paths: Iterable[str]) -> dict[str, list[dict]]:
    docs: list[dict] = []
    links: list[dict] = []
    id_paths: dict[str, list[str]] = defaultdict(list)
    issues: list[dict] = []
    for rel_path in sorted(set(doc_paths)):
        path = repo_root / rel_path
        text, issue = safe_read_text(path, max_bytes=24 * 1024 * 1024)
        if text is None:
            issues.append({"path": rel_path, "issue": issue or "unreadable"})
            continue
        frontmatter, body, fm_issue = _frontmatter(text)
        note_id = str(frontmatter.get("id") or "")
        if not note_id:
            match = _ID_LINE_RE.search(text)
            note_id = match.group(1) if match else ""
        if note_id:
            id_paths[note_id].append(rel_path)
        headings = [{"level": len(markers), "text": title.strip()} for markers, title in _HEADING_RE.findall(body)]
        docs.append({
            "path": rel_path,
            "note_id": note_id or None,
            "title": frontmatter.get("title") or (headings[0]["text"] if headings else Path(rel_path).stem),
            "type": frontmatter.get("type"),
            "status": frontmatter.get("status"),
            "version": str(frontmatter.get("version")) if frontmatter.get("version") is not None else None,
            "domain": frontmatter.get("domain"),
            "heading_count": len(headings),
            "wikilink_count": len(_WIKI_RE.findall(text)),
            "markdown_link_count": len(_MARKDOWN_LINK_RE.findall(text)),
            "frontmatter_present": bool(frontmatter),
            "frontmatter_issue": fm_issue,
            "owner_domain": owner_domain(rel_path),
        })
        for raw in _WIKI_RE.findall(text):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
            links.append({"source_path": rel_path, "target": target, "kind": "wikilink"})
        for raw in _MARKDOWN_LINK_RE.findall(text):
            target = raw.strip().split("#", 1)[0]
            links.append({"source_path": rel_path, "target": target, "kind": "markdown_link"})
    collisions = [
        {"note_id": note_id, "paths": sorted(paths), "path_count": len(paths)}
        for note_id, paths in sorted(id_paths.items())
        if len(paths) > 1
    ]
    return {
        "documents": sorted(docs, key=lambda x: x["path"]),
        "links": sorted(links, key=lambda x: (x["source_path"], x["kind"], x["target"])),
        "collisions": collisions,
        "issues": sorted(issues, key=lambda x: x["path"]),
    }


def scan_schemas(repo_root: Path, candidate_paths: Iterable[str]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    issues: list[dict] = []
    for rel_path in sorted(set(candidate_paths)):
        path = repo_root / rel_path
        suffix = path.suffix.lower()
        lower = rel_path.lower()
        name = path.name.lower()
        if not ("schema" in lower or suffix in {".xsd", ".proto"}):
            continue
        text, issue = safe_read_text(path, max_bytes=16 * 1024 * 1024)
        if text is None:
            issues.append({"path": rel_path, "issue": issue or "unreadable"})
            continue
        schema_type = "unknown_schema"
        title = None
        schema_id = None
        version = None
        required_count = None
        property_count = None
        parse_issue = None
        try:
            if suffix == ".json" or name.endswith(".schema.json"):
                obj = json.loads(text)
                if isinstance(obj, dict):
                    schema_type = "json_schema" if "$schema" in obj or "properties" in obj else "json_contract"
                    title = obj.get("title")
                    schema_id = obj.get("$id") or obj.get("id")
                    version = obj.get("version")
                    required_count = len(obj.get("required", [])) if isinstance(obj.get("required"), list) else None
                    property_count = len(obj.get("properties", {})) if isinstance(obj.get("properties"), dict) else None
            elif suffix in {".yaml", ".yml"}:
                obj = yaml.safe_load(text)
                schema_type = "yaml_schema_or_contract"
                if isinstance(obj, dict):
                    title = obj.get("title") or obj.get("name")
                    schema_id = obj.get("$id") or obj.get("id")
                    version = obj.get("version")
                    required_count = len(obj.get("required", [])) if isinstance(obj.get("required"), list) else None
                    property_count = len(obj.get("properties", {})) if isinstance(obj.get("properties"), dict) else None
            elif suffix == ".xsd":
                schema_type = "xml_schema"
            elif suffix == ".proto":
                schema_type = "protobuf_schema"
        except Exception as exc:
            parse_issue = f"parse_error:{type(exc).__name__}"
        rows.append({
            "path": rel_path,
            "schema_type": schema_type,
            "schema_id": schema_id,
            "title": title,
            "version": str(version) if version is not None else None,
            "required_count": required_count,
            "property_count": property_count,
            "parse_issue": parse_issue,
            "owner_domain": owner_domain(rel_path),
        })
    return sorted(rows, key=lambda x: x["path"]), sorted(issues, key=lambda x: x["path"])


def scan_path_references(repo_root: Path, paths: Iterable[str]) -> tuple[list[dict], list[dict]]:
    """Scan executable/configuration text for repository-relative path consumers.

    Markdown links are handled by ``scan_documents``.  This scanner intentionally
    uses a line-oriented parser instead of one large regular expression so it is
    bounded on generated manifests and large legacy configuration files.
    """
    rows: list[dict] = []
    issues: list[dict] = []
    delimiters = set("\t\r\n\"'`<>|,;()[]{}")
    for rel_path in sorted(set(paths)):
        path = repo_root / rel_path
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            if path.stat().st_size > 8 * 1024 * 1024:
                continue
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                seen: set[tuple[str, int]] = set()
                for line_number, line in enumerate(handle, 1):
                    if not any(prefix in line for prefix in PATH_REFERENCE_PREFIXES):
                        continue
                    for prefix in PATH_REFERENCE_PREFIXES:
                        offset = 0
                        while True:
                            index = line.find(prefix, offset)
                            if index < 0:
                                break
                            end = index + len(prefix)
                            while end < len(line) and line[end] not in delimiters:
                                end += 1
                            raw = line[index:end].rstrip(".:=-").replace("\\", "/")
                            key = (raw, line_number)
                            if len(raw) > len(prefix) and key not in seen:
                                seen.add(key)
                                rows.append({
                                    "source_path": rel_path,
                                    "target_path_text": raw,
                                    "line": line_number,
                                    "target_exists": (repo_root / raw).exists(),
                                    "source_owner_domain": owner_domain(rel_path),
                                })
                            offset = max(end, index + len(prefix))
        except Exception as exc:
            issues.append({"path": rel_path, "issue": f"read_error:{type(exc).__name__}"})
    return sorted(rows, key=lambda x: (x["source_path"], x["line"], x["target_path_text"])), sorted(issues, key=lambda x: x["path"])
