from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'lab/11_strategy_factory/python/saed_v4_execution_twin'
forbidden=('OrderSend(','trade.Buy(','trade.Sell(','activate_runtime = True','select_treatment = True','shadow_replacement": True')
errors=[]
for p in P.glob('*.py'):
 t=p.read_text()
 for token in forbidden:
  if token in t:errors.append(f'{p.name}:{token}')
if errors:raise SystemExit('boundary violations: '+','.join(errors))
print('SAED V4-09 authority boundary passed')
