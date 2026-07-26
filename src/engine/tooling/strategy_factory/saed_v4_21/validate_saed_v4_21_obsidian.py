from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__)
bases=[
    ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_21',
    ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_21',
]
files=sorted(p for b in bases for p in b.rglob('*.md'))
assert len(files)>=100
for p in files:
    t=p.read_text(encoding='utf-8')
    assert t.startswith('---\n')
    assert '\ntitle:' in t[:500]
    assert '\nstatus:' in t[:500]
    assert '\n# ' in t
    assert ('runtime authority' in t.lower() or 'execution authority' in t.lower() or 'research-only' in t.lower())
print(json.dumps({'passed':True,'obsidian_notes':len(files)},sort_keys=True))
