#!/usr/bin/env python3
from __future__ import annotations
import csv, json, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv)>1 else 'docs/strategy_factory_universal_context_exploitation_engine/implementation_program')
repo = root.parents[2]
mach = repo / 'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation'
errors=[]
required_docs=[
 '00_IMPLEMENTATION_PROGRAM_MOC.md','01_IMPLEMENTATION_PROGRAM_CHARTER.md','02_CURRENT_STATE_REUSE_AND_GAP_MAP.md',
 '03_DEPENDENCY_GRAPH_AND_CRITICAL_PATH.md','04_RELEASE_TRAINS_AND_PHASE_MAP.md','05_PHASE_DELIVERY_PROTOCOL.md',
 '17_KICKOFF_AND_FIRST_30_COMMITS.md']
for name in required_docs:
    if not (root/name).exists(): errors.append(f'missing doc: {name}')
program_path=mach/'PROGRAM_V3.json'
if not program_path.exists(): errors.append('missing PROGRAM_V3.json')
else:
    p=json.loads(program_path.read_text(encoding='utf-8'))
    phases=p.get('phases',[])
    if len(phases)!=19: errors.append(f'expected 19 phases, got {len(phases)}')
    ids=[x['id'] for x in phases]
    if len(ids)!=len(set(ids)): errors.append('duplicate phase IDs')
    for ph in phases:
        doc=root/'phases'/f"{ph['slug']}.md"
        if not doc.exists(): errors.append(f'missing phase doc: {doc.name}')
        if len(ph.get('work_packages',[]))<5: errors.append(f"too few work packages: {ph['id']}")
        if len(ph.get('gates',[]))<4: errors.append(f"too few gates: {ph['id']}")
    graph=json.loads((mach/'DEPENDENCY_GRAPH_V3.json').read_text())
    for node, reqs in graph['requires'].items():
        if node not in ids: errors.append(f'unknown graph node: {node}')
        for r in reqs:
            if r not in ids: errors.append(f'unknown dependency {r} for {node}')
    with (mach/'WORK_PACKAGES_V3.csv').open(encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    expected=sum(len(x['work_packages']) for x in phases)
    if len(rows)!=expected: errors.append(f'work package count mismatch {len(rows)} != {expected}')
if errors:
    print('UCEE implementation program validation: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('UCEE implementation program validation: PASS')
