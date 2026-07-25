from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_16.json').read_text())
assert s['phase']=='SAED_V4_16' and s['implementation_status']=='implemented_reference_synthetic' and s['qa']['passed']
assert s['claims']['distributional_survival_tail_boundary_implemented'] and not s['claims']['production_authorization'] and not s['claims']['causal_claim']
print('SAED V4-16 status validation passed')
