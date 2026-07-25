#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
errors: list[str] = []
phase = root / 'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02'
python_root = phase / 'python/fp_i02_kernel'
mql_root = root / 'mql5/Include/FaerieProtocol/EXP0019/Core'

forbidden_tokens = (
    'OrderSend', 'CTrade', 'PositionOpen', 'PositionClose', 'WebRequest', 'socket.', 'requests.',
    'ObjectCreate', 'CopyRates(', 'CopyTicks(', 'HistorySelect(', 'SymbolInfoTick(',
)
for path in list(python_root.glob('*.py')) + list(mql_root.glob('*.mqh')):
    text = path.read_text(encoding='utf-8')
    for token in forbidden_tokens:
        if token in text:
            errors.append(f'forbidden authority/history token {token!r} in {path.relative_to(root)}')

index = root / 'releases/history/exp0019/indexes/EXP0019_FP_I02_FILE_INDEX.txt'
if index.exists():
    forbidden_prefixes = (
        'lab/10_infrastructure/EXP0017_', 'lab/10_infrastructure/EXP0018_',
        'mql5/Include/AlphaLab/', 'mql5/Experts/EXP0017', 'mql5/Experts/EXP0018',
    )
    for relative in index.read_text(encoding='utf-8').splitlines():
        if relative.startswith(forbidden_prefixes):
            errors.append(f'patch owns forbidden previous-context path: {relative}')

if not (root / 'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01/artifacts/FP_I01_ADAPTER_REGISTRY.v1.json').is_file():
    errors.append('FP-I01 adapter registry dependency is missing')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('FP-I02 boundary guard PASS: no history, drawing, broker, order, position, network, or previous-core ownership.')
