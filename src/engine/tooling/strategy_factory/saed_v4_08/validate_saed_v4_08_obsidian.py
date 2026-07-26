from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__);dirs=[ROOT/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_08',ROOT/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_08'];files=sorted(p for d in dirs for p in d.glob('*.md'))
if len(files)<85:raise SystemExit('insufficient Obsidian documentation')
for p in files:
 t=p.read_text()
 if not t.startswith('---\n') or '\n# ' not in t:raise SystemExit(f'invalid note: {p}')
 if len(t.splitlines())<35:raise SystemExit(f'note too short: {p}')
print(f'{len(files)} Obsidian notes validated')
