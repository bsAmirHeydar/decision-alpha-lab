from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__)
bases=[ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_20',ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_20']
files=sorted(f for b in bases for f in b.glob('*.md'));assert len(files)>=140
targets={f.stem for f in ROOT.glob('docs/**/*.md')}
broken=[]
for f in files:
    t=f.read_text(encoding='utf-8')
    assert t.startswith('---\n') and '\n# ' in t and 'status:' in t and 'version:' in t
    for raw in re.findall(r'\[\[([^\]]+)\]\]',t):
        target=raw.split('|',1)[0].split('#',1)[0].strip()
        if target and target not in targets:broken.append((str(f.relative_to(ROOT)),target))
assert not broken,broken[:20]
print(f'SAED V4-20 Obsidian validation passed: {len(files)} notes, 0 broken links')
