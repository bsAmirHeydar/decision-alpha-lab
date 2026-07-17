import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];out=json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_41/reference_output.json').read_text())
assert out['authority']['may_submit_live_order'] is False
assert out['authority']['may_activate_capital'] is False
assert out['authority']['may_reinstate_without_new_qualification'] is False
assert out['release']['production_authorized'] is False
assert out['certificate']['production_authorized'] is False
assert out['handoff']['production_authorized'] is False
assert out['actions']['live_order_side_effects']==0
assert out['retirement']['live_order_side_effects']==0
assert out['handoff']['roadmap_complete'] is True
print('SAED V4-41 authority and program-closure boundary passed')
