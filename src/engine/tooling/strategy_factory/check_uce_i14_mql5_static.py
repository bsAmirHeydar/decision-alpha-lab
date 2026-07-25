#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/ImmutableRuntime'
FILES=sorted(INC.glob('UCEI14_*.mqh'))+[ROOT/'mql5/Experts/StrategyFactory/UCE_I14_ImmutableRuntimeDiagnostic.mq5',ROOT/'mql5/Tests/Experts/StrategyFactory/UCE_I14_PreprocessingParitySelfTest.mq5',ROOT/'mql5/Tests/Experts/StrategyFactory/UCE_I14_AtomicActivationRollbackSelfTest.mq5',ROOT/'mql5/Tests/Experts/StrategyFactory/UCE_I14_DuplicateDecisionKillSwitchSelfTest.mq5'];errors=[]
if len(FILES)!=16:errors.append(f'expected 16 MQL5 files, found {len(FILES)}')
for p in FILES:
 if not p.exists():errors.append(f'missing {p.relative_to(ROOT)}');continue
 text=p.read_text(encoding='utf-8')
 for token in ('OrderSend(', 'CTrade', '.Buy(', '.Sell(', 'WebRequest(', 'PositionOpen('):
  if token in text:errors.append(f'{p.relative_to(ROOT)} contains forbidden {token}')
 if p.suffix=='.mq5' and '#property strict' not in text:errors.append(f'{p.relative_to(ROOT)} missing #property strict')
for name,tokens in {'UCEI14_Gate.mqh':('bundle_not_activatable','kill_switch','duplicate_request','order_authority=false'),'UCEI14_Generation.mqh':('UCEI14_VALIDATED','UCEI14_RETIRED','signature_valid','parity_pass'),'UCEI14_Preprocessing.mqh':('unknown_category','(score-0.5)/0.25'),'UCEI14_Model.mqh':('enter_long','no_action'),'UCEI14_Catalog.mqh':('return(13)','approved_native_v1')}.items():
 text=(INC/name).read_text()
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I14 MQL5 static checks: PASS ({len(FILES)} files; MetaEditor compile not asserted)')
