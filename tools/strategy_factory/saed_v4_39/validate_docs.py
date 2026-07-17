from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];phase=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_39';atomic=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_39';pd=list(phase.glob('*.md'));ad=list(atomic.glob('*.md'));assert len(pd)>=24;assert len(ad)>=96
for p in pd+ad:
 s=p.read_text(encoding='utf-8');assert s.startswith('---\n');assert 'SAED V4-39' in s;assert len(s)>600
print(f'SAED V4-39 docs: {len(pd)} phase + {len(ad)} atomic passed')
