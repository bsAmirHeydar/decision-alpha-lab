from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];bases=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_18',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_18']
files=[f for b in bases for f in b.glob('*.md')];assert len(files)>=80
names={f.stem for b in bases for f in b.glob('*.md')}
for f in files:
 text=f.read_text(encoding='utf-8');assert text.startswith('---\n') and 'title:' in text and '# ' in text and 'SAED V4-18' in text
 for token in __import__('re').findall(r'\[\[([^\]|#]+)',text):
  if token.startswith('00_MOC_V4_18') or token in names:continue
print(f'SAED V4-18 Obsidian validation passed: {len(files)} notes')
