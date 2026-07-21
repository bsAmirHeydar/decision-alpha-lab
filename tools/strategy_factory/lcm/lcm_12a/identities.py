from __future__ import annotations
import re
from pathlib import Path

_ID_PATTERN=re.compile(r"\b[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]{4,})+\b")
_PHASE_PATTERN=re.compile(r"\b(?:LCM|ACL(?:_OS)?|SAED|UCEE|EXP|FP)[-_][A-Z0-9_.-]+\b")

def collect_valid_entity_ids(repo_root:Path):
    ids=set()
    for path in repo_root.rglob("*"):
        rel=path.relative_to(repo_root).as_posix()
        if rel.startswith(("registry/legacy_context_migration/documentation_authority_mappings/","registry/legacy_context_migration/lcm_12a/")):continue
        for part in path.parts:
            stem=Path(part).stem
            if _ID_PATTERN.fullmatch(stem):ids.add(stem)
        if path.is_file() and path.suffix.lower()==".json" and path.stat().st_size<=200_000 and (rel.startswith("registry/legacy_context_migration/") or rel.startswith("registry/acl_os/")):
            text=path.read_text(encoding="utf-8",errors="ignore")
            ids.update(_ID_PATTERN.findall(text))
    ids.update({"LCM-12A","LCM-12B","LCM-11B","LCM-10C","LCM_ROADMAP_R1_BALANCED_PARTITION"})
    return ids

def extract_entity_refs(text:str,valid_ids:set[str]):
    tokens=set(_ID_PATTERN.findall(text))|set(_PHASE_PATTERN.findall(text))
    valid=sorted(token for token in tokens if token in valid_ids or token.startswith(("LCM-","ACL-","SAED-","UCEE-","EXP-")))
    unknown=sorted(tokens-set(valid))
    return valid,unknown
