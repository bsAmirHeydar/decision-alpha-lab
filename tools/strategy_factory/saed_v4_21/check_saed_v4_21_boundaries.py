from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]
base=ROOT/'lab/11_strategy_factory/python/saed_v4_robust_optimization_regret'
forbidden=[
    'OrderSend(',
    'CTrade ',
    'WebRequest(',
    'import MetaTrader5',
    'mt5.order_send',
    'production_authorization = True',
    'runtime_executable = True',
]
viol=[]
for p in base.glob('*.py'):
    t=p.read_text(encoding='utf-8')
    for tok in forbidden:
        if tok in t:
            viol.append(f'{p.name}:{tok}')
assert not viol,viol
print(json.dumps({'passed':True,'boundary_violations':0},sort_keys=True))
