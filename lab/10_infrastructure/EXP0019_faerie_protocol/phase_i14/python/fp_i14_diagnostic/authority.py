from pathlib import Path
from .constants import FORBIDDEN_TOKENS

def scan_forbidden(paths):
    hits=[]
    for p in map(Path,paths):
        if not p.exists() or not p.is_file(): continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        for token in FORBIDDEN_TOKENS:
            if token in text:hits.append((str(p),token))
    return tuple(hits)
