#!/usr/bin/env python3
from pathlib import Path
import ast
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
phase = root / 'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i08'
errors: list[str] = []

for path in (phase / 'python/fp_i08_weekly').glob('*.py'):
    text = path.read_text(encoding='utf-8')
    for token in (
        'OrderSend(', 'CTrade', 'PositionOpen(', 'ObjectCreate(', 'ChartCreate',
        'WebRequest(', 'requests.', 'socket.', 'MetaTrader5'
    ):
        if token in text:
            errors.append(f'forbidden authority {token} in {path.relative_to(root)}')
    ast.parse(text)

index = root / 'releases/history/exp0019/indexes/EXP0019_FP_I08_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text(encoding='utf-8').splitlines():
        if any(f'/phase_i0{i}/' in rel for i in range(8)):
            errors.append('phase owns upstream implementation path ' + rel)

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('FP-I08 boundary guard PASS: weekly context only; no drawing, order, broker, position, or network authority.')
