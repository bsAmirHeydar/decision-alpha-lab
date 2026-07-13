#!/usr/bin/env python3
from pathlib import Path
import ast
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
phase = root / 'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i07'
py = phase / 'python/fp_i07_confirmation'

for path in py.glob('*.py'):
    text = path.read_text(encoding='utf-8')
    for token in ('OrderSend(', 'CTrade', 'PositionOpen', 'ObjectCreate(', 'ChartCreate', 'WebRequest(', 'requests.', 'socket.', 'MetaTrader5'):
        if token in text:
            errors.append(f'forbidden authority {token} in {path.relative_to(root)}')
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or '']
            for name in names:
                if name.startswith(('fp_i00', 'fp_i01')):
                    errors.append(f'forbidden direct dependency {name}')

index = root / 'EXP0019_FP_I07_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text(encoding='utf-8').splitlines():
        if any(f'/phase_i0{i}/' in rel for i in range(7)) or rel.startswith(('mql5/Include/DayeTrader/', 'lab/10_infrastructure/EXP0018_')):
            errors.append('phase owns upstream path ' + rel)

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('FP-I07 boundary guard PASS: confirmation-only authority; no WW, drawing, trading, broker, position, or network authority.')
