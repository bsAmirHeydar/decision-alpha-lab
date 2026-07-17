from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];dirs=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_35',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_35'];files=[p for d in dirs for p in d.glob('*.md')]
assert len(files)>=200
for p in files:
 t=p.read_text(encoding='utf-8');assert t.startswith('---\n');assert 'phase: SAED_V4_35' in t;assert len(t)>700
print(f'V4-35 Obsidian validation passed: {len(files)} notes')
