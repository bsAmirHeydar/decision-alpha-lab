from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_18.json').read_text(encoding='utf-8'))
assert s['implementation_status']=='implemented_reference_synthetic' and s['next_phase']=='SAED_V4_19' and s['qa']['passed']
assert s['claims']['causal_treatment_policy_value_boundary_implemented'] and not s['claims']['real_treatment_effect_established'] and not s['claims']['real_policy_value_established'] and not s['claims']['production_authorization'] and not s['claims']['live_trading']
assert s['external_evidence']['metaeditor_compile']=='pending_local_windows'
print('SAED V4-18 phase status validation passed')
