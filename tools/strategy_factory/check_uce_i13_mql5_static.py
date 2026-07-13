#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/HybridPolicy'
FILES=sorted(INC.glob('UCEI13_*.mqh'))+[ROOT/'mql5/Experts/StrategyFactory/UCE_I13_HybridPolicyDiagnostic.mq5',ROOT/'mql5/Experts/StrategyFactoryTests/UCE_I13_ManualParitySelfTest.mq5',ROOT/'mql5/Experts/StrategyFactoryTests/UCE_I13_AuthorityFallbackSelfTest.mq5']
errors=[]
if len(FILES)!=12:errors.append(f'expected 12 MQL5 files, found {len(FILES)}')
for p in FILES:
    if not p.exists():errors.append(f'missing {p.relative_to(ROOT)}');continue
    text=p.read_text(encoding='utf-8')
    for token in ('OrderSend(', 'CTrade', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
        if token in text:errors.append(f'{p.relative_to(ROOT)} contains forbidden {token}')
    if p.suffix=='.mq5' and '#property strict' not in text:errors.append(f'{p.relative_to(ROOT)} missing #property strict')
cat=(INC/'UCEI13_Catalog.mqh').read_text()
if 'return 14;' not in cat or cat.count('case ')!=14:errors.append('catalog must contain 14 deterministic node kinds')
a=(INC/'UCEI13_Authority.mqh').read_text()
if not a.index('if(kill_switch)')<a.index('if(risk_rejected)')<a.index('if(operator_veto)')<a.index('if(manual_veto)'):errors.append('MQL5 authority precedence mismatch')
g=(INC/'UCEI13_Gate.mqh').read_text()
for token in ('signed_promote','model.stale','model.ood','model.low_confidence','model.missing_view','UCEI13_MANUAL_ONLY'):
    if token not in g:errors.append(f'gate missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I13 MQL5 static checks: PASS ({len(FILES)} files; MetaEditor compile not asserted)')
