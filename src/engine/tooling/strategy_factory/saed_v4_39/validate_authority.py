from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);out=json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_39/reference_output.json').read_text())
assert out['authority_boundary']['may_submit_live_order'] is False
assert out['stage_qualification']['micro_live_eligible'] is False
assert out['release_candidate']['order_submission_allowed'] is False
assert out['release_candidate']['capital_activation_allowed'] is False
assert out['certificate']['production_authorized'] is False
assert out['handoff']['production_authorized'] is False
print('SAED V4-39 authority boundary passed')
