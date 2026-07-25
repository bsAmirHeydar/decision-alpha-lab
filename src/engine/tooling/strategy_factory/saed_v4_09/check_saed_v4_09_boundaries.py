from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);P=ROOT/'src/engine/packages/saed_v4_execution_twin'
forbidden=('OrderSend(','trade.Buy(','trade.Sell(','activate_runtime = True','select_treatment = True','shadow_replacement": True')
errors=[]
for p in P.glob('*.py'):
 t=p.read_text()
 for token in forbidden:
  if token in t:errors.append(f'{p.name}:{token}')
if errors:raise SystemExit('boundary violations: '+','.join(errors))
print('SAED V4-09 authority boundary passed')
