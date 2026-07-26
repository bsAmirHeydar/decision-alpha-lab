from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__);folders=[ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_23',ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_23'];files=[p for f in folders for p in f.glob('*.md')]
assert len(files)>=180
for p in files:
    t=p.read_text(encoding='utf-8');assert t.startswith('---\n') and '# ' in t and 'SAED V4-23' in t and len(t)>=1200,p
print(f'V4-23 Obsidian validation passed: {len(files)} notes')
