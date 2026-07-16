from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_21.json').read_text())
assert s['phase']=='SAED_V4_21' and s['status']=='reference_implementation_complete'
assert s['claims']['robust_optimization_implemented'] and s['claims']['regret_analysis_implemented'] and s['claims']['baseline_preservation_implemented']
assert not s['claims']['real_policy_value_established'] and not s['claims']['production_treatment_selection'] and not s['claims']['production_risk_allocation'] and not s['claims']['production_authorization']
assert not any(s['authority'].values())
print(json.dumps({'passed':True,'phase':s['phase']},sort_keys=True))
