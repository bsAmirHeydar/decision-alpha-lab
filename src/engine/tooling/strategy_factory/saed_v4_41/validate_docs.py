from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);phase=ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_41';atomic=ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_41';pd=list(phase.glob('*.md'));ad=list(atomic.glob('*.md'));assert len(pd)>=40;assert len(ad)>=170
for p in pd+ad:
 s=p.read_text(encoding='utf-8');assert s.startswith('---\n');assert 'SAED V4-41' in s;assert len(s)>1000
print(f'SAED V4-41 docs: {len(pd)} phase + {len(ad)} atomic passed')
