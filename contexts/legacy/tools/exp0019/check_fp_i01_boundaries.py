#!/usr/bin/env python3
from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=[root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01',root/'mql5/Include/FaerieProtocol/EXP0019/Compatibility',root/'mql5/Experts/FaerieProtocol',root/'mql5/Tests/Experts/FaerieProtocol']
errors=[]
for base in owned:
    for p in base.rglob('*'):
        if not p.is_file() or p.suffix not in {'.py','.mqh','.mq5','.ps1'}:continue
        if p.name.startswith('test_') or p.name in {'duplicate_scan.py','check_fp_i01_boundaries.py'}:continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        tokens=['Order'+'Send','C'+'Trade','Position'+'Open','Web'+'Request','Socket'+'Create']
        for token in tokens:
            if token in text:errors.append(f'forbidden authority {token}: {p.relative_to(root)}')
        if p.suffix in {'.mqh','.mq5'} and re.search(r'(NthSunday|SecondSunday|FirstSunday|NewYork.*Offset)',text,re.I):
            errors.append(f'duplicate New York time implementation: {p.relative_to(root)}')
index=root/'releases/history/exp0019/indexes/EXP0019_FP_I01_FILE_INDEX.txt'
if index.exists():
    paths=index.read_text().splitlines()
    for prefix in ('mql5/Include/IntermarketDivergenceExecution/CG/','mql5/Include/DayeTrader/EXP0018/'):
        if any(x.startswith(prefix) for x in paths):errors.append(f'shared-core file owned by patch: {prefix}')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('FP-I01 boundary guard PASS: read-only adapters, no shared-core ownership, no runtime authority, no duplicate time core.')
