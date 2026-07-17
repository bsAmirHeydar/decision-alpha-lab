import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_portfolio_execution_economics.constitution import authority_boundary
x=authority_boundary(); denied=['may_send_order','may_activate_capital','may_mutate_ucee','may_promote_model','may_compile_live_runtime','production_authorization','live_trading_authority']
if any(x[k] for k in denied):raise SystemExit('authority expansion detected')
print(json.dumps({'phase':'SAED_V4_37','denied':denied,'passed':True}))
