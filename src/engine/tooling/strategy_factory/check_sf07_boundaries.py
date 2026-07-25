#!/usr/bin/env python3
from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=[root/'mql5/Include/AlphaLab/StrategyFactory/Context',root/'mql5/Experts/StrategyFactory/SF07_StrategyHost.mq5',root/'mql5/Experts/StrategyFactory/SF07_ContextDiagnostic.mq5',root/'mql5/Tests/Experts/StrategyFactory/SF07_ContextEngineSelfTest.mq5']
forbidden=['LongToString(','OrderSend(','OrderCheck(','CTrade','PositionOpen(','EXP0017','Daye']
errors=[]
for p in owned:
    paths=list(p.rglob('*')) if p.is_dir() else [p]
    for f in paths:
        if not f.is_file() or f.suffix.lower() not in {'.mqh','.mq5'}:continue
        text=f.read_text(encoding='utf-8',errors='ignore')
        clean=re.sub(r'/\*.*?\*/','',text,flags=re.S);clean=re.sub(r'//.*','',clean)
        for token in forbidden:
            if token in clean:errors.append(f'{f.relative_to(root)}: forbidden token {token}')
print(f'SF07 boundary guard: errors={len(errors)}')
for e in errors:print('ERROR',e)
raise SystemExit(1 if errors else 0)
