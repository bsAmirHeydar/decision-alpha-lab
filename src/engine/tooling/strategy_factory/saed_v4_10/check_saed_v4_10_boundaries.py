from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
paths=list((ROOT/'src/engine/packages/saed_v4_baseline_manual').glob('*.py'))+list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_10').glob('*.mqh'))
forbidden=['OrderSend(','CTrade','PositionOpen(','strategy_factory_execution','strategy_factory_live','activate_runtime = True','send_order = True']
violations=[]
for p in paths:
 text=p.read_text(errors='ignore')
 for token in forbidden:
  if token in text:violations.append(f'{p.relative_to(ROOT)}::{token}')
if violations:raise SystemExit('boundary violations\n'+'\n'.join(violations))
print(f'boundary guard passed for {len(paths)} files')
