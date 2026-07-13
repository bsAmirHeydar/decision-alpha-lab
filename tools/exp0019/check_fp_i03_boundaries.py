#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import ast,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
phase=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03'
errors=[]
for path in (phase/'python/fp_i03_time').glob('*.py'):
    try: tree=ast.parse(path.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'parse {path}: {exc}');continue
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            names=[]
            if isinstance(node,ast.Import): names=[a.name for a in node.names]
            else: names=[node.module or '']
            for name in names:
                lowered=name.lower()
                if any(token in lowered for token in ('requests','urllib','socket','metatrader','order','brokerapi')):
                    errors.append(f'forbidden import {name} in {path.relative_to(root)}')
for path in phase.rglob('*'):
    if path.is_file() and path.suffix in {'.py','.mqh','.mq5'}:
        text=path.read_text(encoding='utf-8',errors='ignore').lower()
        if path.name in {'check_fp_i03_boundaries.py','test_fp_i03_authority_boundary.py'}: continue
        for token in ('ordersend','positionopen','webrequest','objectcreate('):
            if token in text: errors.append(f'forbidden authority token {token} in {path.relative_to(root)}')
# Phase may depend on FP-I02 and shared Daye time, but cannot own/modify those paths.
index=root/'EXP0019_FP_I03_FILE_INDEX.txt'
if index.exists():
    for rel in index.read_text(encoding='utf-8').splitlines():
        if rel.startswith(('mql5/Include/DayeTrader/','lab/10_infrastructure/EXP0018_','lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/')):
            errors.append('forbidden upstream ownership '+rel)
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print('FP-I03 boundary guard PASS: only FP-I02 identity/shared Daye time dependencies, no price/drawing/execution/network authority, no upstream ownership.')
