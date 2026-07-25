from __future__ import annotations
from pathlib import Path
import re
FORBIDDEN_IMPL_PATTERNS={
 'NEW_YORK_DST_REIMPLEMENTATION':re.compile(r'(NthSunday|SecondSunday|FirstSunday|NewYork.*Offset)',re.I),
 'ORDER_AUTHORITY':re.compile(r'\b(OrderSend|CTrade|PositionOpen|Buy\s*\(|Sell\s*\(|WebRequest)\b'),
 'FULL_HISTORY_LOOP':re.compile(r'for\s*\([^;]*;[^;]*(Bars|iBars)\s*\(',re.I),
}
ALLOWED_NAMES={'FP_I01_StaticGuard.mqh'}

def scan_paths(repo:Path,relative_roots):
    findings=[]
    for rel in relative_roots:
        base=repo/rel
        if not base.exists():continue
        for p in base.rglob('*'):
            if not p.is_file() or p.suffix not in {'.mqh','.mq5','.py'}:continue
            if p.name == 'duplicate_scan.py' or p.name.startswith('test_'): continue
            text=p.read_text(encoding='utf-8',errors='ignore')
            for code,pattern in FORBIDDEN_IMPL_PATTERNS.items():
                if pattern.search(text): findings.append({'code':code,'path':p.relative_to(repo).as_posix()})
    return tuple(sorted(findings,key=lambda x:(x['code'],x['path'])))
