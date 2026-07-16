from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3];dirs=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_15',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_15'];files=[p for d in dirs for p in d.glob('*.md')];assert files
for p in files:
 t=p.read_text(encoding='utf-8');assert t.startswith('---\n') and '\n# ' in t and len(t)>900,p;assert not re.search(r'\]\(sandbox:',t),p
print(f'SAED V4-15 Obsidian validation passed: {len(files)} notes')
