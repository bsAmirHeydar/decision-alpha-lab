from tools.repository_paths import find_repository_root
from pathlib import Path
import re,yaml
ROOT=find_repository_root(__file__);folders=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_04',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_04']
notes=[p for f in folders for p in f.glob('*.md')];titles={};names={p.stem for p in ROOT.rglob('*.md')};errors=[]
for p in notes:
 text=p.read_text()
 if not text.startswith('---\n'):errors.append(f'frontmatter missing: {p}');continue
 parts=text.split('---\n',2);meta=yaml.safe_load(parts[1]);title=meta.get('title')
 if not title:errors.append(f'title missing: {p}')
 if title in titles:errors.append(f'duplicate title: {title}')
 titles[title]=p
 for link in re.findall(r'\[\[([^]|#]+)',text):
  if link not in names:errors.append(f'broken link {link} in {p.name}')
if errors:raise SystemExit('\n'.join(errors))
print(f'validated {len(notes)} notes, 0 broken links, 0 duplicate titles')
