from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];targets=[ROOT/'lab/11_strategy_factory/python/saed_v4_outcome_cube',ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4OutcomeCube'];forbidden=('OrderSend(','WebRequest(','requests.get(','requests.post(','socket.','subprocess.','train_model(','.fit(','allocate_risk(')
viol=[]
for base in targets:
 for p in base.rglob('*'):
  if p.suffix.lower() not in ('.py','.mqh','.mq5'):continue
  text=p.read_text(errors='ignore')
  for token in forbidden:
   if token in text:viol.append(f'{p.relative_to(ROOT)}:{token}')
if viol:raise SystemExit('boundary violations: '+';'.join(viol))
print('SAED V4-08 boundary guard passed')
