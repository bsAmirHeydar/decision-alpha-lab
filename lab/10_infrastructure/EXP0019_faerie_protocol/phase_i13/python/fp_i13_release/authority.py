from pathlib import Path
from .constants import FORBIDDEN_AUTHORITIES

def scan_paths(paths):
    findings=[]
    for path in paths:
        p=Path(path)
        if not p.exists():continue
        for f in ([p] if p.is_file() else p.rglob('*')):
            if not f.is_file() or f.suffix.lower() not in ('.py','.mq5','.mqh','.md','.json','.csv','.ps1'):continue
            text=f.read_text(encoding='utf-8',errors='ignore')
            for token in FORBIDDEN_AUTHORITIES:
                if token in text and 'FORBIDDEN_AUTHORITIES' not in text and 'forbidden' not in f.name.lower(): findings.append((str(f),token))
    return tuple(findings)
