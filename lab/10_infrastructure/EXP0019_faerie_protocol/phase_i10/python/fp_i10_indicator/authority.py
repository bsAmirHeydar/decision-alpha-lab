from pathlib import Path
from .constants import FORBIDDEN_MQL5_TOKENS

def scan_mql5_authority(paths):
    hits=[]
    for path in map(Path,paths):
        text=path.read_text(encoding='utf-8',errors='ignore')
        for token in FORBIDDEN_MQL5_TOKENS:
            if token in text: hits.append((path.as_posix(),token))
    return tuple(hits)
