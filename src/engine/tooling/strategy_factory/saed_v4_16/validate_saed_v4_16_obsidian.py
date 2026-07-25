from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__)
dirs=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_16',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_16']
files=[p for d in dirs for p in d.glob('*.md')]
assert files
for p in files:
    t=p.read_text(encoding='utf-8')
    assert t.startswith('---\n') and '\n# ' in t and len(t)>1200,p
    assert not re.search(r'\]\(sandbox:',t),p
print(f'SAED V4-16 Obsidian validation passed: {len(files)} notes')
