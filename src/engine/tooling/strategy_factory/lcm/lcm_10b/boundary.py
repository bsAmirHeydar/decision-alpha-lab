from __future__ import annotations
from pathlib import Path
from .constants import FORBIDDEN_BROKER_TOKENS
APPROVED_PREFIXES=("src/engine/tooling/strategy_factory/lcm/lcm_10b/","mql5/Include/StrategyFactory/LCM/V10B/","mql5/Experts/StrategyFactory/LCM/V10B/")
def scan_canonical_boundary(repo_root:Path)->dict:
    hits=[]
    for prefix in APPROVED_PREFIXES:
        root=repo_root/prefix
        if not root.exists():continue
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".py",".mqh",".mq5"}:continue
            if p.name in {"constants.py","boundary.py"}:continue
            text=p.read_text(encoding="utf-8",errors="replace")
            for token in FORBIDDEN_BROKER_TOKENS:
                if token in text:hits.append({"path":p.relative_to(repo_root).as_posix(),"token":token})
    return {"passed":not hits,"hit_count":len(hits),"hits":hits,"approved_prefixes":list(APPROVED_PREFIXES)}
