from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__);bases=[ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_19',ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_19']
files=[f for b in bases for f in b.glob('*.md')];assert len(files)>=100
names={f.stem for b in bases for f in b.glob('*.md')}
for f in files:
 text=f.read_text(encoding='utf-8');assert text.startswith('---\n') and 'title:' in text and '# ' in text and 'SAED V4-19' in text
print(f'SAED V4-19 Obsidian validation passed: {len(files)} notes')
