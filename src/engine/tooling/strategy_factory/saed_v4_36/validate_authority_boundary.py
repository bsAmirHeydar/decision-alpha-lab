from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);a=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_AUTHORITY.JSON').read_text());c=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_CERTIFICATE.JSON').read_text());h=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_HANDOFF.JSON').read_text());p=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36/GOLDEN_PLAN.JSON').read_text())
for k in ['may_execute_experiment','may_mutate_ucee','may_select_treatment','may_allocate_capital','may_compile_live_runtime','may_send_order','promotion_authority','production_authorization','live_trading_authority']:assert a[k] is False
assert c['production_authorized'] is False and c['runtime_activation_allowed'] is False and c['automatic_execution_authorized'] is False
assert h['authority_granted'] is False and h['capital_authority_granted'] is False and h['execution_authority_granted'] is False
assert p['automatic_execution_allowed'] is False
print('V4-36 authority boundary passed')
