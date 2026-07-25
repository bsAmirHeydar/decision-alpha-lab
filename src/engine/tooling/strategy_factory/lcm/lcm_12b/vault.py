from __future__ import annotations
from collections import defaultdict
from pathlib import Path, PurePosixPath
from .frontmatter import heading_anchors
from .links import build_basename_index, resolve_markdown, resolve_wiki, _MD, _WIKI

def scan_links(repo_root: Path, paths: list[str], existing_paths: set[str]):
    basename = build_basename_index(existing_paths)
    edges: list[dict] = []
    unresolved: list[dict] = []
    anchor_cache: dict[str, set[str]] = {}
    for relative in sorted(set(paths)):
        path = repo_root / relative
        if not path.is_file() or path.suffix.lower() not in (".md", ".mdx", ".rst", ".txt", ".adoc"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in _MD.finditer(text):
            raw = match.group(2)
            target, anchor, _ = resolve_markdown(relative, raw, existing_paths)
            if not target or target not in existing_paths:
                if raw.strip().startswith(("http://", "https://", "mailto:", "data:", "#")):
                    continue
                unresolved.append({"source_path": relative, "kind": "MARKDOWN", "raw_target": raw, "resolved_candidate": target, "reason": "TARGET_MISSING"})
                continue
            anchor_value = anchor[1:].lower() if anchor.startswith("#") else ""
            anchor_ok = True
            if anchor_value and target.lower().endswith((".md", ".mdx")):
                if target not in anchor_cache:
                    anchor_cache[target] = heading_anchors((repo_root / target).read_text(encoding="utf-8", errors="replace"))
                anchor_ok = anchor_value in anchor_cache[target]
            if not anchor_ok:
                unresolved.append({"source_path": relative, "kind": "MARKDOWN", "raw_target": raw, "resolved_candidate": target, "reason": "HEADING_MISSING"})
            edges.append({"source_path": relative, "target_path": target, "kind": "MARKDOWN", "anchor_status": "PASS" if anchor_ok else "FAILED"})
        for match in _WIKI.finditer(text):
            raw = match.group(2)
            target, anchor, _ = resolve_wiki(raw, relative, existing_paths, basename)
            if not target:
                unresolved.append({"source_path": relative, "kind": "WIKI", "raw_target": raw, "resolved_candidate": None, "reason": "UNRESOLVED_OR_AMBIGUOUS"})
                continue
            anchor_value = anchor[1:].lower() if anchor.startswith("#") else ""
            anchor_ok = True
            if anchor_value and target.lower().endswith((".md", ".mdx")):
                if target not in anchor_cache:
                    anchor_cache[target] = heading_anchors((repo_root / target).read_text(encoding="utf-8", errors="replace"))
                anchor_ok = anchor_value in anchor_cache[target]
            if not anchor_ok:
                unresolved.append({"source_path": relative, "kind": "WIKI", "raw_target": raw, "resolved_candidate": target, "reason": "HEADING_MISSING"})
            edges.append({"source_path": relative, "target_path": target, "kind": "WIKI", "anchor_status": "PASS" if anchor_ok else "FAILED"})
    return edges, unresolved

def basename_collisions(paths: set[str]):
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in sorted(paths):
        grouped[PurePosixPath(path).name.lower()].append(path)
    return {name: values for name, values in grouped.items() if len(values) > 1}
