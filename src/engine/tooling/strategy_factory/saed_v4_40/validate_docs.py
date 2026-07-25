from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);phase=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_40';atomic=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_40';pd=list(phase.glob('*.md'));ad=list(atomic.glob('*.md'));assert len(pd)>=28;assert len(ad)>=120
for p in pd+ad:
 s=p.read_text(encoding='utf-8');assert s.startswith('---\n');assert 'SAED V4-40' in s;assert len(s)>900
print(f'SAED V4-40 docs: {len(pd)} phase + {len(ad)} atomic passed')
