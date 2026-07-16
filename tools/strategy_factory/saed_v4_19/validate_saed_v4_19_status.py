from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_19.json').read_text(encoding='utf-8'))
assert s['phase']=='SAED_V4_19' and s['implementation_status']=='implemented_reference_synthetic' and s['qa']['passed']
for k in ['real_setup_validity_established','real_mechanism_established','real_policy_value_established','production_treatment_selection','promotion_authorization','runtime_activation','production_authorization','live_trading']:assert s['claims'][k] is False
assert not any(s['authority'][k] for k in ['decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])
print('SAED V4-19 phase status validation passed')
