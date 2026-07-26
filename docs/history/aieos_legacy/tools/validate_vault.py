#!/usr/bin/env python3
"""Validate the AI Algorithm Engineering OS Obsidian vault.

Checks:
- Markdown frontmatter and unique IDs for normative notes
- Internal wiki-link resolution
- Duplicate relative paths (case-insensitive)
- Empty markdown files
- Unresolved template placeholders outside templates/prompts/examples

Usage:
    python tools/validate_vault.py [vault_path]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

WIKI = re.compile(r"\[\[([^\]]+)\]\]")
ID_RE = re.compile(r"^id:\s*([^\s]+)\s*$", re.M)
PLACEHOLDER = re.compile(r"\[(?:authoritative|exact|precise|name|owner|title|task|link|text|paths?|commands?|facts?|assumptions?|unknowns?|risks?|x\.y\.z|ALG-\.\.\.|PATCH-ID|TEST-ID|NNNN|YYYY-MM-DD|\.\.\.)[^\]]*\]", re.I)
SKIP_FRONTMATTER = {'README.md','README_FA.md','AGENTS.md','MASTER_PLAYBOOK.md','INSTALLATION.md','CHANGELOG.md'}
PLACEHOLDER_ALLOWED = {'08_PROMPT_LIBRARY','14_TEMPLATES','16_EXAMPLES'}


def normalize_target(raw: str) -> str:
    target = raw.split('|',1)[0].split('#',1)[0].strip().replace('\\','/')
    if target.endswith('.md'):
        target = target[:-3]
    return target.strip('/')


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    if not root.is_dir():
        print(f'ERROR: vault not found: {root}')
        return 2

    md_files = sorted(root.rglob('*.md'))
    errors: list[str] = []
    warnings: list[str] = []
    ids: dict[str, Path] = {}
    path_index: dict[str, Path] = {}
    basename_index: dict[str, list[Path]] = {}

    for p in md_files:
        rel = p.relative_to(root).as_posix()
        key = rel.lower()
        if key in path_index:
            errors.append(f'case-insensitive duplicate path: {rel} / {path_index[key].relative_to(root)}')
        path_index[key] = p
        basename_index.setdefault(p.stem.lower(), []).append(p)

        text = p.read_text(encoding='utf-8')
        if not text.strip():
            errors.append(f'empty markdown file: {rel}')
        if p.name not in SKIP_FRONTMATTER and not text.startswith('---\n'):
            errors.append(f'missing frontmatter: {rel}')
        m = ID_RE.search(text)
        if m:
            note_id = m.group(1)
            if note_id in ids:
                errors.append(f'duplicate id {note_id}: {rel} / {ids[note_id].relative_to(root)}')
            ids[note_id] = p
        elif p.name not in SKIP_FRONTMATTER:
            errors.append(f'missing id: {rel}')

        if not any(part in PLACEHOLDER_ALLOWED for part in p.parts):
            for match in PLACEHOLDER.finditer(text):
                warnings.append(f'possible unresolved placeholder in {rel}: {match.group(0)}')

    stem_paths = {p.relative_to(root).with_suffix('').as_posix().lower(): p for p in md_files}
    for p in md_files:
        text = p.read_text(encoding='utf-8')
        rel = p.relative_to(root).as_posix()
        for raw in WIKI.findall(text):
            target = normalize_target(raw)
            if not target or target.startswith(('http://','https://')):
                continue
            tkey = target.lower()
            if tkey in stem_paths:
                continue
            # Obsidian also resolves unique basenames.
            base = Path(target).name.lower()
            matches = basename_index.get(base, [])
            if len(matches) == 1:
                continue
            if len(matches) > 1:
                errors.append(f'ambiguous wikilink in {rel}: [[{raw}]]')
            else:
                errors.append(f'broken wikilink in {rel}: [[{raw}]]')

    print(f'Vault: {root}')
    print(f'Markdown notes: {len(md_files)}')
    print(f'Unique note IDs: {len(ids)}')
    print(f'Errors: {len(errors)}')
    print(f'Warnings: {len(warnings)}')
    for item in errors[:100]:
        print('ERROR:', item)
    for item in warnings[:30]:
        print('WARN :', item)
    if len(errors) > 100:
        print(f'... {len(errors)-100} additional errors omitted')
    if len(warnings) > 30:
        print(f'... {len(warnings)-30} additional warnings omitted')
    return 1 if errors else 0

if __name__ == '__main__':
    raise SystemExit(main())
