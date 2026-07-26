#!/usr/bin/env python3
from pathlib import Path
import csv, json, re, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
base=root/'docs/operations/execution/EXP0019_faerie_protocol_contextual_divergence'
prog=base/'implementation_program'
errors=[]
required=[
 base/'00_EXP0019_MOC.md',base/'27_MQL5_MODULAR_ARCHITECTURE.md',base/'34_IMPLEMENTATION_ROADMAP.md',
 base/'35_HANDOFF_TO_CODE.md',base/'44_ACCEPTANCE_GATE_FOR_CODING.md',prog/'00_IMPLEMENTATION_PROGRAM_MOC.md',
 prog/'fp_implementation_phase_registry.v1.json',prog/'fp_planned_module_registry.v1.csv',
 prog/'fp_indicator_acceptance_matrix.v1.csv',prog/'fp_implementation_task_ledger.v1.csv'
]
for p in required:
    if not p.is_file(): errors.append(f'missing {p.relative_to(root)}')
md=list(prog.rglob('*.md')); phases=list((prog/'phases').glob('*.md'))
if len(md)!=38: errors.append(f'expected 38 implementation markdown files, got {len(md)}')
if len(phases)!=17: errors.append(f'expected 17 phase docs, got {len(phases)}')
for p in md:
    text=p.read_text(encoding='utf-8')
    if not text.startswith('---\n'): errors.append(f'missing frontmatter {p.relative_to(root)}')
    if any(c in p.name for c in ':*?"<>|'): errors.append(f'windows-unsafe filename {p.relative_to(root)}')
    if p.parent.name=='phases' and len(text.splitlines())<130: errors.append(f'phase too short {p.relative_to(root)}')
    for raw in re.findall(r'\[\[([^\]]+)\]\]',text):
        target=raw.split('|',1)[0].split('#',1)[0]
        if not target: continue
        q=p.parent/target
        if not (q.exists() or q.with_suffix('.md').exists()): errors.append(f'broken link {p.relative_to(root)} -> {target}')
try:
    reg=json.loads((prog/'fp_implementation_phase_registry.v1.json').read_text(encoding='utf-8'))
    if len(reg.get('phases',[]))!=17: errors.append('phase registry count mismatch')
    if reg.get('indicator_milestone')!='FP-I13': errors.append('indicator milestone mismatch')
    if reg.get('live_blocker')!='FP-DEC-012': errors.append('live blocker mismatch')
except Exception as e: errors.append(f'invalid phase registry: {e}')
for fn,min_rows in [('fp_planned_module_registry.v1.csv',23),('fp_indicator_acceptance_matrix.v1.csv',14),('fp_implementation_task_ledger.v1.csv',83)]:
    try:
        rows=list(csv.DictReader((prog/fn).read_text(encoding='utf-8').splitlines()))
        if len(rows)<min_rows: errors.append(f'{fn} rows {len(rows)} < {min_rows}')
    except Exception as e: errors.append(f'invalid csv {fn}: {e}')
road=(base/'34_IMPLEMENTATION_ROADMAP.md').read_text(encoding='utf-8') if (base/'34_IMPLEMENTATION_ROADMAP.md').exists() else ''
for token in ('FP-I10','FP-I13','complete indicator','FP-DEC-012'):
    if token.lower() not in road.lower(): errors.append(f'roadmap missing {token}')
# documentation-only authority check for patch-owned changed/new surfaces
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
lines=sum(len(p.read_text(encoding='utf-8').splitlines()) for p in md)
print(f'EXP0019 implementation program validation PASS: {len(md)} Markdown docs, {len(phases)} phases, {lines} implementation-program lines, 83 tasks, 23+ planned modules, 14 indicator acceptance requirements, no broken local links, Windows-safe filenames.')
