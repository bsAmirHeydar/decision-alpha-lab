from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_17.json').read_text())
assert s['phase']=='SAED_V4_17' and s['implementation_status']=='implemented_reference_synthetic'
assert s['claims']['causal_mechanism_discovery_boundary_implemented'] and not s['claims']['real_causal_mechanism_discovered'] and not s['claims']['treatment_effect_identified'] and not s['claims']['production_authorization']
assert s['authority']['research_reference_only'] and not any(s['authority'][k] for k in ['causal_claim_authority','decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])
print('SAED V4-17 phase status validation passed')
