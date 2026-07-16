from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3];bases=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_17',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_17']
files=[p for b in bases for p in b.glob('*.md')];assert len(files)>=80
for p in files:
 t=p.read_text(encoding='utf-8');assert t.startswith('---\n') and '\n# ' in t and 'SAED V4-17' in t and len(t)>900,p
print(f'SAED V4-17 Obsidian validation passed: {len(files)} notes')
