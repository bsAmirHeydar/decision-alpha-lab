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
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body

def heading_anchors(text: str) -> set[str]:
    _, body = split_frontmatter(text)
    anchors = set()
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        value = re.sub(r"[`*_~]", "", match.group(1).strip().lower())
        value = re.sub(r"[^\w\-\s]", "", value, flags=re.UNICODE)
        value = re.sub(r"\s+", "-", value).strip("-")
        if value:
            anchors.add(value)
    return anchors
