#!/usr/bin/env python3
from pathlib import Path
import ast,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
phase=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04'
py=phase/'python/fp_i04_data'
for path in py.glob('*.py'):
    text=path.read_text(encoding='utf-8')
    for token in ('OrderSend(','CTrade','PositionOpen','ObjectCreate(','ChartCreate','WebRequest(','socket.','requests.','MetaTrader5'):
        if token in text:errors.append(f'forbidden authority token {token} in {path.relative_to(root)}')
    tree=ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            names=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or '']
            for name in names:
                if name.startswith(('fp_i00','fp_i01')):errors.append(f'forbidden direct dependency {name} in {path.relative_to(root)}')
index=root/'EXP0019_FP_I04_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text().splitlines():
        if any(f'/phase_i0{i}/' in rel for i in range(4)) or rel.startswith('mql5/Include/DayeTrader/'):
            errors.append('phase owns upstream path '+rel)
if not (phase/'artifacts/FP_I04_HANDOFF_TO_FP_I05.json').exists():errors.append('handoff missing')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('FP-I04 boundary guard PASS: phase-local data plane, exact I02/I03 upstream dependencies, no relation/drawing/trading/network authority.')
