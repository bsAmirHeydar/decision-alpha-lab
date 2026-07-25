from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);dirs=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_36',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_36'];files=[p for d in dirs for p in d.glob('*.md')]
assert len(files)>=220
for p in files:
 t=p.read_text(encoding='utf-8');assert t.startswith('---\n');assert 'phase: SAED_V4_36' in t;assert len(t)>700
print(f'V4-36 Obsidian validation passed: {len(files)} notes')
