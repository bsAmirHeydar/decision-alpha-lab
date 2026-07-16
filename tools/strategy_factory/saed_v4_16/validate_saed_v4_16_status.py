from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_16.json').read_text())
assert s['phase']=='SAED_V4_16' and s['implementation_status']=='implemented_reference_synthetic' and s['qa']['passed']
assert s['claims']['distributional_survival_tail_boundary_implemented'] and not s['claims']['production_authorization'] and not s['claims']['causal_claim']
print('SAED V4-16 status validation passed')
