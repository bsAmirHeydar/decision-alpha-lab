#!/usr/bin/env python3
"""Static MQL5 contract checks; this is not a MetaEditor compile claim."""
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
INCLUDE=ROOT/'mql5'/'Include'/'AlphaLab'/'StrategyFactory'/'ExperimentOrchestration'
FILES=sorted(INCLUDE.glob('UCEI11_*.mqh'))+[
 ROOT/'mql5'/'Experts'/'StrategyFactory'/'UCE_I11_ExperimentOrchestrationDiagnostic.mq5',
 ROOT/'mql5'/'Experts'/'StrategyFactoryTests'/'UCE_I11_ExperimentContractsSelfTest.mq5',
 ROOT/'mql5'/'Experts'/'StrategyFactoryTests'/'UCE_I11_BudgetAndReproSelfTest.mq5',
]
errors=[]
if len(FILES)!=11: errors.append(f'expected 11 MQL5 files, found {len(FILES)}')
for path in FILES:
    if not path.exists(): errors.append(f'missing: {path.relative_to(ROOT)}'); continue
    text=path.read_text(encoding='utf-8')
    for token in ('OrderSend(', 'CTrade', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
        if token in text: errors.append(f'{path.relative_to(ROOT)} contains forbidden {token}')
    if '#property strict' not in text and path.suffix=='.mq5':
        errors.append(f'{path.relative_to(ROOT)} missing #property strict')
catalog=(INCLUDE/'UCEI11_Catalog.mqh').read_text(encoding='utf-8')
if 'return 10;' not in catalog: errors.append('catalog count is not 10')
if catalog.count('case ')!=10: errors.append(f'catalog case count is {catalog.count("case ")} not 10')
registry=(INCLUDE/'UCEI11_Registry.mqh').read_text(encoding='utf-8')
for token in ('BuildDefault','Freeze','ResolveExact','NativeCount'):
    if token not in registry: errors.append(f'registry missing {token}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'UCE-I11 MQL5 static checks: PASS ({len(FILES)} files; MetaEditor compile not asserted)')
