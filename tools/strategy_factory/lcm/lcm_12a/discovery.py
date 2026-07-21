from __future__ import annotations
import re
from pathlib import Path
from .canonical import file_digest, sha256_text, stable_id
from .constants import DOCUMENT_EXTENSIONS, EXCLUDED_PARTS, SELF_EXCLUDED_PREFIXES, SELF_EXCLUDED_ROOT_PREFIXES
from .frontmatter import split_frontmatter, first_heading, heading_anchors

_DYNAMIC_FRONTMATTER = {"updated", "generated_at", "generated_time", "timestamp", "digest", "sha256", "hash"}

def is_excluded(rel: str, parts: tuple[str, ...]) -> bool:
    if any(part in EXCLUDED_PARTS for part in parts):
        return True
    if any(rel.startswith(prefix) for prefix in SELF_EXCLUDED_PREFIXES):
        return True
    name = parts[-1] if parts else rel
    return any(name.startswith(prefix) for prefix in SELF_EXCLUDED_ROOT_PREFIXES)

def normalize_text(text: str) -> str:
    frontmatter, body = split_frontmatter(text)
    fm_lines = []
    for key in sorted(frontmatter):
        if key.lower() in _DYNAMIC_FRONTMATTER:
            continue
        value = frontmatter[key]
        if isinstance(value, list):
            value = ",".join(sorted(str(x).strip() for x in value))
        fm_lines.append(f"{key.strip().lower()}:{str(value).strip()}")
    lines = [re.sub(r"[ \t]+$", "", line) for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    collapsed = []
    blank = 0
    for line in lines:
        if line.strip():
            blank = 0; collapsed.append(line.strip())
        else:
            blank += 1
            if blank <= 1: collapsed.append("")
    return "\n".join(fm_lines + [""] + collapsed).strip() + "\n"

def topic_key(title: str, path: str) -> str:
    raw = title or Path(path).stem
    raw = re.sub(r"\b(v(?:ersion)?\s*\d+(?:\.\d+)*)\b", "", raw, flags=re.I)
    tokens = re.findall(r"[a-z0-9]+", raw.lower())
    stop = {"the", "and", "or", "of", "for", "to", "a", "an", "readme", "install", "rollback", "commit", "message", "report", "patch"}
    tokens = [token for token in tokens if token not in stop]
    return "_".join(tokens[:16]) or Path(path).stem.lower()

def discover_documents(repo_root: Path):
    rows = []
    for path in sorted(repo_root.rglob("*"), key=lambda p: p.as_posix().lower()):
        if not path.is_file() or path.suffix.lower() not in DOCUMENT_EXTENSIONS:
            continue
        rel = path.relative_to(repo_root).as_posix()
        if is_excluded(rel, path.relative_to(repo_root).parts):
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        frontmatter, body = split_frontmatter(text)
        title = str(frontmatter.get("title") or first_heading(body) or path.stem).strip()
        version = str(frontmatter.get("version") or frontmatter.get("schema_version") or "UNVERSIONED")
        status = str(frontmatter.get("status") or "UNSPECIFIED")
        normalized = normalize_text(text)
        row = {
            "document_id": stable_id("DOC", rel, file_digest(path)),
            "path": rel,
            "extension": path.suffix.lower(),
            "size_bytes": len(raw),
            "line_count": text.count("\n") + 1,
            "byte_digest": file_digest(path),
            "normalized_digest": sha256_text(normalized),
            "title": title,
            "topic_key": topic_key(title, rel),
            "declared_version": version,
            "declared_status": status,
            "frontmatter_keys": sorted(frontmatter.keys()),
            "heading_anchors": sorted(heading_anchors(body)),
            "active": not any(token in rel.lower().split("/") for token in ("archive", "archived", "attic", "backup", "backups")),
            "text": text,
            "normalized_text": normalized,
            "body": body,
        }
        rows.append(row)
    return rows

def corpus_digest(rows):
    payload = [{"path": row["path"], "byte_digest": row["byte_digest"], "normalized_digest": row["normalized_digest"]} for row in rows]
    return sha256_text(__import__("json").dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
