from tools.repository_paths import find_repository_root
from pathlib import Path
import re,json
ROOT=find_repository_root(__file__);dirs=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_22',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_22'];files=sorted(p for d in dirs for p in d.glob('*.md'))
assert len(files)>=150
names={p.stem for p in files}
for p in files:
    t=p.read_text(encoding='utf-8');assert t.startswith('---\n') and '# ' in t and 'SAED V4-22' in t
    for link in re.findall(r'\[\[([^\]|#]+)',t):
        if link.startswith('V4_22_') or link in names:assert link in names,(p.name,link)
print(json.dumps({'passed':True,'obsidian_notes':len(files)},sort_keys=True))
