from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_18.json').read_text(encoding='utf-8'))
assert s['implementation_status']=='implemented_reference_synthetic' and s['next_phase']=='SAED_V4_19' and s['qa']['passed']
assert s['claims']['causal_treatment_policy_value_boundary_implemented'] and not s['claims']['real_treatment_effect_established'] and not s['claims']['real_policy_value_established'] and not s['claims']['production_authorization'] and not s['claims']['live_trading']
assert s['external_evidence']['metaeditor_compile']=='pending_local_windows'
print('SAED V4-18 phase status validation passed')
