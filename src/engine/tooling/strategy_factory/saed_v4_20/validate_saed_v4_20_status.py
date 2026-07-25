from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__)
s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_20.json').read_text(encoding='utf-8'))
assert s['phase']=='SAED_V4_20' and s['implementation_status']=='implemented_reference_synthetic'
assert s['claims']['decision_focused_selection_implemented'] and s['claims']['set_valued_selection_implemented'] and s['claims']['selection_certificate_implemented']
assert not s['claims']['real_policy_value_established'] and not s['claims']['production_treatment_selection'] and not s['claims']['production_authorization'] and not s['claims']['live_trading']
assert not any(s['authority'][k] for k in ['real_policy_value_claim_authority','production_treatment_selection_authority','decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])
assert s['qa']['passed'] and s['qa']['golden_reproduction']
print('SAED V4-20 phase status validation passed')
