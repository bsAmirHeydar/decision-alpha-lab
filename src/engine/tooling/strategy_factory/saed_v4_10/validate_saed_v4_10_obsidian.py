from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);dirs=[ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_10',ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_10'];files=[p for d in dirs for p in d.glob('*.md')]
assert len(files)>=63
for p in files:
 t=p.read_text(encoding='utf-8');assert t.startswith('---\n');assert '# ' in t;assert 'SAED V4-10' in t or 'V4-10' in t
print(f'{len(files)} Obsidian notes validated')
