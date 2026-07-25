#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/ContextTournament'
FILES=sorted(INC.glob('UCEI15_*.mqh'))+[ROOT/'mql5/Experts/StrategyFactory/UCE_I15_ContextTournamentDiagnostic.mq5',ROOT/'mql5/Tests/Experts/StrategyFactory/UCE_I15_FixtureCannotPromoteSelfTest.mq5',ROOT/'mql5/Tests/Experts/StrategyFactory/UCE_I15_FreezeAndCountSelfTest.mq5',ROOT/'mql5/Tests/Experts/StrategyFactory/UCE_I15_ProspectiveReconciliationSelfTest.mq5'];errors=[]
if len(FILES)!=14:errors.append(f'expected 14 MQL5 files, found {len(FILES)}')
for p in FILES:
 if not p.exists():errors.append(f'missing {p.relative_to(ROOT)}');continue
 text=p.read_text(encoding='utf-8')
 for token in ('OrderSend(', 'CTrade', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
  if token in text:errors.append(f'{p.relative_to(ROOT)} contains forbidden {token}')
 if p.suffix=='.mq5' and '#property strict' not in text:errors.append(f'{p.relative_to(ROOT)} missing #property strict')
checks={'UCEI15_Catalog.mqh':('return(9)','return(8)','partial_plus_runner'),'UCEI15_Inventory.mqh':('require_real','UCEI15_FIXTURE'),'UCEI15_Gate.mqh':('tournament_not_reference_only','paper_mode_prospective','UCEI15_REJECT'),'UCEI15_Boundary.mqh':('return(false)','ReferenceFixtureMayPromote')}
for name,tokens in checks.items():
 text=(INC/name).read_text()
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I15 MQL5 static checks: PASS ({len(FILES)} files; MetaEditor compile not asserted)')
