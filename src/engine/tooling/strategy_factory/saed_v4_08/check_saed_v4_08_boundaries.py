from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);targets=[ROOT/'src/engine/packages/saed_v4_outcome_cube',ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4OutcomeCube'];forbidden=('OrderSend(','WebRequest(','requests.get(','requests.post(','socket.','subprocess.','train_model(','.fit(','allocate_risk(')
viol=[]
for base in targets:
 for p in base.rglob('*'):
  if p.suffix.lower() not in ('.py','.mqh','.mq5'):continue
  text=p.read_text(errors='ignore')
  for token in forbidden:
   if token in text:viol.append(f'{p.relative_to(ROOT)}:{token}')
if viol:raise SystemExit('boundary violations: '+';'.join(viol))
print('SAED V4-08 boundary guard passed')
