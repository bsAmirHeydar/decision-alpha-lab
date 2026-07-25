from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);out=json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_40/reference_output.json').read_text())
assert out['authority']['may_submit_live_order'] is False
assert out['authority']['may_cross_tenant_route'] is False
assert out['release']['live_order_submission_allowed'] is False
assert out['release']['capital_activation_allowed'] is False
assert out['certificate']['production_authorized'] is False
assert out['handoff']['production_authorized'] is False
assert out['control_journal']['live_order_side_effects']==0
print('SAED V4-40 authority boundary passed')
