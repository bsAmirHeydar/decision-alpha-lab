from tools.repository_paths import find_repository_root
from pathlib import Path
import re
ROOT=find_repository_root(__file__);docs=list((ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_13').glob('*.md'))+list((ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_13').glob('*.md'))+[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/60_IMPLEMENTATION_PROGRAM_V4/V4_13_Graph_And_Hypergraph_Models.md'];names={p.stem for p in (ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4').rglob('*.md')}
broken=[]
for p in docs:
 text=p.read_text(encoding='utf-8');assert text.startswith('---') and '# ' in text
 for target in re.findall(r'\[\[([^\]|#]+)',text):
  if target not in names:broken.append((p.name,target))
assert not broken,broken[:20]
print(f'validated {len(docs)} SAED V4-13 Obsidian notes with zero broken wikilinks')
