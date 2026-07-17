import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];a=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_35/GOLDEN_AUTHORITY.JSON').read_text());c=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_35/GOLDEN_CERTIFICATE.JSON').read_text());h=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_35/GOLDEN_HANDOFF.JSON').read_text())
for k in ['may_mutate_ucee','may_select_treatment','may_allocate_risk','may_compile_live_runtime','may_send_order','promotion_authority','production_authorization','live_trading_authority']:assert a[k] is False
assert c['production_authorized'] is False and c['runtime_activation_allowed'] is False;assert h['authority_granted'] is False
print('V4-35 authority boundary passed')
