from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__);roots=[ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_12',ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_12'];files=[p for r in roots for p in r.rglob('*.md')]
assert files
for p in files:
 t=p.read_text(encoding='utf-8');assert t.startswith('---\n') and '\n# ' in t and 'SAED V4-12' in t,(p,'frontmatter/title')
 assert 'Authority boundary' in t or 'Authority Boundary' in t,(p,'authority boundary section')
print(f'V4-12 Obsidian validation passed: {len(files)} notes')
