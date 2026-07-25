from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
paths=list((ROOT/'src/engine/packages/saed_v4_self_supervised_pretraining').glob('*.py'))+list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_11').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_11').glob('*.mq5'))
forbidden=['OrderSend(','CTrade','PositionOpen(','activate_runtime = True','send_order = True','use_outcome_cube_as_input": True','execution_authority": True']
violations=[]
for p in paths:
 text=p.read_text(encoding='utf-8',errors='ignore')
 for token in forbidden:
  if token in text:violations.append(f'{p.relative_to(ROOT)}::{token}')
if violations:raise SystemExit('boundary violations\n'+'\n'.join(violations))
print(f'V4-11 boundary guard passed for {len(paths)} files')
