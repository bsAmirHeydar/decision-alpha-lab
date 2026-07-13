#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/ContextOnboarding'
FILES=sorted(INC.glob('UCEI16_*.mqh'))+[ROOT/'mql5/Experts/StrategyFactory/UCE_I16_ContextOnboardingDiagnostic.mq5',ROOT/'mql5/Experts/StrategyFactoryTests/UCE_I16_ScaffoldIdentitySelfTest.mq5',ROOT/'mql5/Experts/StrategyFactoryTests/UCE_I16_LegacyParitySelfTest.mq5',ROOT/'mql5/Experts/StrategyFactoryTests/UCE_I16_CoreInvarianceSelfTest.mq5'];errors=[]
if len(FILES)!=17:errors.append(f'expected 17 MQL5 files, found {len(FILES)}')
for p in FILES:
 if not p.exists():errors.append(f'missing {p.relative_to(ROOT)}');continue
 text=p.read_text(encoding='utf-8')
 for token in ('OrderSend(', 'CTrade', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
  if token in text:errors.append(f'{p.relative_to(ROOT)} contains forbidden {token}')
 if p.suffix=='.mq5' and '#property strict' not in text:errors.append(f'{p.relative_to(ROOT)} missing #property strict')
checks={'UCEI16_Catalog.mqh':('return 2','return 6','return 4'),'UCEI16_Boundary.mqh':('return false','return true'),'UCEI16_Invariance.mqh':('UCEI16_ADR_REQUIRED','changed_core_count'),'UCEI16_TournamentTemplate.mqh':('fixture_not_alpha_proof','stage_count==9')}
for name,tokens in checks.items():
 text=(INC/name).read_text()
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I16 MQL5 static checks: PASS ({len(FILES)} files; MetaEditor compile not asserted)')
