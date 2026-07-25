from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);phase=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_38';atomic=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_38';pd=list(phase.glob('*.md'));ad=list(atomic.glob('*.md'))
if len(pd)<130 or len(ad)<110:raise SystemExit(f'docs incomplete {len(pd)} {len(ad)}')
for p in pd+ad:
 s=p.read_text(encoding='utf-8').lower()
 for token in ['saed v4-38','research-only','immutable']:
  if token not in s:raise SystemExit(f'{p}: missing {token}')
print(json.dumps({'phase':'SAED_V4_38','phase_docs':len(pd),'atomic_docs':len(ad),'passed':True}))
