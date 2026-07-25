from __future__ import annotations
import re

def split_frontmatter(text: str):
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        return {}, normalized
    end = normalized.find("\n---\n", 4)
    if end < 0:
        return {}, normalized
    raw = normalized[4:end]
    body = normalized[end + 5:]
    data = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip(); value = value.strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            value = [part.strip().strip('"').strip("'") for part in value[1:-1].split(",") if part.strip()]
        data[key] = value
    return data, body

def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None

def heading_anchors(body: str) -> set[str]:
    anchors = set()
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        title = match.group(1).strip().lower()
        title = re.sub(r"[`*_~]", "", title)
        title = re.sub(r"[^\w\-\s]", "", title, flags=re.UNICODE)
        title = re.sub(r"\s+", "-", title).strip("-")
        if title:
            anchors.add(title)
    return anchors
