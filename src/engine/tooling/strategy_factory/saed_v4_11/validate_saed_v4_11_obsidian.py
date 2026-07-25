from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__)
roots=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_11',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_11']
files=[p for r in roots for p in r.glob('*.md')]
assert len(files)>=90
all_md=list((ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4').rglob('*.md'))
stems={p.stem for p in all_md};names={p.name for p in all_md}
broken=[]
for p in files:
 text=p.read_text(encoding='utf-8')
 assert text.startswith('---\n')
 for raw in re.findall(r'\[\[([^\]]+)\]\]',text):
  target=raw.split('|',1)[0].split('#',1)[0].strip()
  if not target:continue
  base=Path(target).name
  if base not in stems and base+'.md' not in names:broken.append(f'{p.relative_to(ROOT)} -> {target}')
if broken:raise SystemExit('broken Obsidian links\n'+'\n'.join(broken[:50]))
print(f'V4-11 Obsidian validation passed: {len(files)} phase/atomic notes, 0 broken links')
