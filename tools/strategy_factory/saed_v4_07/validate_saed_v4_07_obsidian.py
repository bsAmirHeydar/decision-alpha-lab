from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3];DOC=ROOT/'docs';P=DOC/'strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_07';A=DOC/'strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_07';phase=sorted(P.glob('*.md'));atomic=sorted(A.glob('*.md'));files=phase+atomic
if len(phase)<64 or len(atomic)<24:raise SystemExit(f'V4-07 docs incomplete phase={len(phase)} atomic={len(atomic)}')
known={p.stem for p in DOC.rglob('*.md')};missing=[]
for p in files:
 t=p.read_text();
 if not t.startswith('---\n') or 'phase: V4-07' not in t or 'status: implemented' not in t:raise SystemExit(f'invalid frontmatter {p}')
 if len(t.splitlines())<35:raise SystemExit(f'underspecified note {p}')
 for raw in re.findall(r'\[\[([^\]]+)\]\]',t):
  target=Path(raw.split('|',1)[0].split('#',1)[0].strip()).name
  if target and target not in known:missing.append((p,target))
if missing:raise SystemExit('broken links: '+';'.join(f'{p}->{t}' for p,t in missing[:20]))
print(f'validated {len(files)} V4-07 Obsidian notes ({len(phase)} phase, {len(atomic)} atomic)')
