from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'lab/11_strategy_factory/python/saed_v4_action_lattice'
forbidden_imports=('strategy_factory_execution','strategy_factory_live','strategy_factory_portfolio','MetaTrader5','requests','httpx','urllib','socket','aiohttp','sklearn','torch','tensorflow','xgboost','lightgbm','catboost')
forbidden_calls={'order_send','OrderSend','send_order','activate_runtime','allocate_risk','select_treatment','fit','predict','train','compile_runtime','WebRequest'}
viol=[];paths=sorted(P.glob('*.py'))
if len(paths)<25:raise SystemExit('V4-07 Python package incomplete')
for p in paths:
 tree=ast.parse(p.read_text(),filename=str(p))
 for n in ast.walk(tree):
  if isinstance(n,ast.Import):
   for a in n.names:
    if a.name.startswith(forbidden_imports):viol.append(f'{p.name}: import {a.name}')
  elif isinstance(n,ast.ImportFrom) and n.module and n.module.startswith(forbidden_imports):viol.append(f'{p.name}: import {n.module}')
  elif isinstance(n,ast.Call):
   name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ''
   if name in forbidden_calls:viol.append(f'{p.name}: call {name}')
if viol:raise SystemExit('; '.join(viol))
print(f'boundary scan passed for {len(paths)} Python modules')
