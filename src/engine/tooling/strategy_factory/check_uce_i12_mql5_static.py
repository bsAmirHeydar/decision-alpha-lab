#!/usr/bin/env python3
"""Static MQL5 contract checks; this is not a MetaEditor compilation claim."""
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
INCLUDE=ROOT/'mql5'/'Include'/'AlphaLab'/'StrategyFactory'/'StatisticalPromotion'
FILES=sorted(INCLUDE.glob('UCEI12_*.mqh'))+[
 ROOT/'mql5'/'Experts'/'StrategyFactory'/'UCE_I12_StatisticalPromotionDiagnostic.mq5',
 ROOT/'mql5'/'Experts'/'StrategyFactoryTests'/'UCE_I12_PromotionContractsSelfTest.mq5',
 ROOT/'mql5'/'Experts'/'StrategyFactoryTests'/'UCE_I12_NonCompensatoryGateSelfTest.mq5',
]
errors=[]
if len(FILES)!=11: errors.append(f'expected 11 MQL5 files, found {len(FILES)}')
for path in FILES:
    if not path.exists(): errors.append(f'missing: {path.relative_to(ROOT)}'); continue
    text=path.read_text(encoding='utf-8')
    for token in ('OrderSend(', 'CTrade', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
        if token in text: errors.append(f'{path.relative_to(ROOT)} contains forbidden {token}')
    if path.suffix=='.mq5' and '#property strict' not in text: errors.append(f'{path.relative_to(ROOT)} missing #property strict')
catalog=(INCLUDE/'UCEI12_Catalog.mqh').read_text(encoding='utf-8')
if 'return 7;' not in catalog: errors.append('catalog count is not 7')
if catalog.count('case ')!=7: errors.append(f'catalog case count is {catalog.count("case ")} not 7')
gate=(INCLUDE/'UCEI12_Gate.mqh').read_text(encoding='utf-8')
for token in ('CriticalBlockers()>0','multiplicity.total_choice_count!=universe.declared_trial_count','mandatory_nulls_passed','prospective_frozen','signed_bundle'):
    if token not in gate: errors.append(f'gate missing {token}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'UCE-I12 MQL5 static checks: PASS ({len(FILES)} files; MetaEditor compile not asserted)')
