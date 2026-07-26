from tools.repository_paths import find_repository_root
import json,re
from pathlib import Path
ROOT=find_repository_root(__file__); phase=ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_37'; atomic=ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_37'; docs=list(phase.glob('*.md'))+list(atomic.glob('*.md'))
if len(list(phase.glob('*.md')))<120 or len(list(atomic.glob('*.md')))<100:raise SystemExit('documentation corpus incomplete')
for p in docs:
 s=p.read_text(encoding='utf-8')
 for token in ['SAED V4-37','research-only']:
  if token.lower() not in s.lower():raise SystemExit(f'{p}: missing {token}')
print(json.dumps({'phase':'SAED_V4_37','phase_docs':len(list(phase.glob("*.md"))),'atomic_docs':len(list(atomic.glob("*.md"))),'passed':True}))
