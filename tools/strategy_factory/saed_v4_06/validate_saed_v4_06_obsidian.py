from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
DOC_ROOT=ROOT/'docs'
PHASE=DOC_ROOT/'strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_06'
ATOMIC=DOC_ROOT/'strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_06'
phase_files=sorted(PHASE.glob('*.md'));atomic_files=sorted(ATOMIC.glob('*.md'));files=phase_files+atomic_files
if len(phase_files)<60 or len(atomic_files)<20 or len(files)<80:
    raise SystemExit(f'V4-06 Obsidian documentation incomplete: phase={len(phase_files)} atomic={len(atomic_files)}')
known={p.stem for p in DOC_ROOT.rglob('*.md')}
missing=[]
for path in files:
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or 'phase: V4-06' not in text or 'status: implemented' not in text:
        raise SystemExit(f'invalid frontmatter: {path.relative_to(ROOT)}')
    if len(text.splitlines())<25:
        raise SystemExit(f'underspecified note: {path.relative_to(ROOT)}')
    for raw in re.findall(r'\[\[([^\]]+)\]\]',text):
        target=Path(raw.split('|',1)[0].split('#',1)[0].strip()).name
        if target and target not in known: missing.append((str(path.relative_to(ROOT)),target))
if missing:
    raise SystemExit('broken Obsidian links: '+'; '.join(f'{a}->{b}' for a,b in missing[:30]))
print(f'validated {len(files)} V4-06 Obsidian notes ({len(phase_files)} phase, {len(atomic_files)} atomic)')
