#!/usr/bin/env python3
"""Static compatibility and authority checks for the UCE-I10 MQL5 mirror.

This is intentionally not a MetaEditor compiler substitute. It provides a fast,
portable preflight and leaves the compile gate pending until Windows logs exist.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
include_root = root / 'mql5/Include/AlphaLab/StrategyFactory/DeepViews'
targets = sorted(include_root.rglob('*.mqh')) + [
    root / 'mql5/Experts/StrategyFactory/UCE_I10_DeepViewsDiagnostic.mq5',
    root / 'mql5/Tests/Experts/StrategyFactory/UCE_I10_DeepViewsSelfTest.mq5',
    root / 'mql5/Tests/Experts/StrategyFactory/UCE_I10_CausalitySafetySelfTest.mq5',
]
errors: list[str] = []
for file in targets:
    if not file.is_file():
        errors.append(f'missing {file.relative_to(root)}')
        continue
    text = file.read_text(encoding='utf-8', errors='ignore')
    for token in ('LongToString(', 'std::', 'nullptr', 'auto ', 'namespace '):
        if token in text:
            errors.append(f'{file.relative_to(root)}: unsupported/undesired token {token}')
    if text.count('{') != text.count('}'):
        errors.append(f'{file.relative_to(root)}: brace imbalance')
    if text.count('(') != text.count(')'):
        errors.append(f'{file.relative_to(root)}: parenthesis imbalance')
    for include in re.findall(r'#include\s+"([^"]+)"', text):
        if not (file.parent / include).exists():
            errors.append(f'{file.relative_to(root)}: missing local include {include}')
    if re.search(r'\b(OrderSend|OrderCheck|PositionOpen|WebRequest|SocketCreate)\s*\(', text):
        errors.append(f'{file.relative_to(root)}: forbidden runtime authority')

catalog = include_root / 'UCEI10_Catalog.mqh'
all_header = include_root / 'UCEI10_All.mqh'
if catalog.exists():
    compact = ''.join(catalog.read_text(encoding='utf-8').split())
    if 'Count(){return17;}' not in compact:
        errors.append('UCEI10_Catalog.mqh: catalog count is not exactly 17')
    if 'NativeCount(){return10;}' not in compact:
        errors.append('UCEI10_Catalog.mqh: native count is not exactly 10')
    if compact.count('"causal_temporal_conv_ridge"') != 1:
        errors.append('UCEI10_Catalog.mqh: canonical sequence descriptor missing/duplicated')
if all_header.exists():
    all_text = all_header.read_text(encoding='utf-8')
    required_includes = (
        'UCEI10_Enums.mqh', 'UCEI10_AlgorithmDescriptor.mqh', 'UCEI10_ViewContracts.mqh',
        'UCEI10_QualificationContracts.mqh', 'UCEI10_RegimeFusionContracts.mqh',
        'UCEI10_DependencyTransferContracts.mqh', 'UCEI10_Catalog.mqh', 'UCEI10_Registry.mqh',
    )
    for include in required_includes:
        if include not in all_text:
            errors.append(f'UCEI10_All.mqh: missing include {include}')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(
    f'UCE-I10 MQL5 static PASS: {len(targets)} files; include closure, delimiter balance, '
    'catalog 17/native 10, compatibility, and no-execution-authority checks passed. '
    'MetaEditor compile remains a separate local-Windows gate.'
)
