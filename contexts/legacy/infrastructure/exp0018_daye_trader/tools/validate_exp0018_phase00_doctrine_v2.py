#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

repo=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
base=repo/'docs/operations/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2/07_phase00_doctrine_freeze_v2'
errors=[]; warnings=[]
required=[base/'00_INDEX.md',base/'01_MASTER_BASELINE.md',base/'15_ARCHITECT_DECISION_WORKBOOK.md',base/'20_DOCTRINE_FREEZE_GATE.md',base/'data/EXP0018_PHASE00_DECISION_LEDGER_V2.csv',base/'data/EXP0018_PHASE00_DOCTRINE_SNAPSHOT_V2.json']
for p in required:
    if not p.exists(): errors.append(f'missing: {p.relative_to(repo)}')
adr=list((base/'adr').glob('ADR-DY-A*.md')) if (base/'adr').exists() else []
if len(adr)!=12: errors.append(f'expected 12 ADRs, found {len(adr)}')
try:
    with open(base/'data/EXP0018_PHASE00_DECISION_LEDGER_V2.csv',encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    ids=[r['decision_id'] for r in rows]
    if len(rows)!=12 or len(set(ids))!=12: errors.append('decision ledger must contain 12 unique decisions')
    allowed={'PROPOSED','ACCEPTED','DEFERRED','REJECTED'}
    for r in rows:
        if r['status'] not in allowed: errors.append(f"invalid decision status {r['decision_id']}: {r['status']}")
        if r['status']=='ACCEPTED' and (not r['approved_by'] or not r['approved_at']): errors.append(f"accepted decision lacks approval: {r['decision_id']}")
except Exception as e: errors.append(f'decision ledger error: {e}')
try:
    with open(base/'data/EXP0018_PHASE00_RELATIONSHIP_SNAPSHOT_V2.csv',encoding='utf-8-sig',newline='') as f: rels=list(csv.DictReader(f))
    if len(rels)!=22: errors.append(f'expected 22 relationships, found {len(rels)}')
    if sum(int(r['major']) for r in rels)!=6: errors.append('expected 6 major relationships')
except Exception as e: errors.append(f'relationship registry error: {e}')
try:
    snap=json.loads((base/'data/EXP0018_PHASE00_DOCTRINE_SNAPSHOT_V2.json').read_text(encoding='utf-8'))
    if snap.get('execution_authority') is not False: errors.append('execution_authority must be false')
    if snap.get('relationship_count')!=22: errors.append('snapshot relationship_count must be 22')
except Exception as e: errors.append(f'snapshot error: {e}')
try:
    with open(base/'data/EXP0018_PHASE00_INVARIANT_REGISTRY_V2.csv',encoding='utf-8-sig',newline='') as f: inv=list(csv.DictReader(f))
    if len(inv)<20: errors.append('expected at least 20 invariants')
except Exception as e: errors.append(f'invariant registry error: {e}')
try:
    with open(base/'data/EXP0018_PHASE00_FIXTURE_REGISTRY_V2.csv',encoding='utf-8-sig',newline='') as f: fx=list(csv.DictReader(f))
    if len(fx)<18: errors.append('expected at least 18 doctrine fixtures')
    covered={r['rule_or_decision'] for r in fx}
    for did in ['DY-A01','DY-A02','DY-A03','DY-A04','DY-A05','DY-A12']:
        if did not in covered: errors.append(f'critical decision missing fixture: {did}')
except Exception as e: errors.append(f'fixture registry error: {e}')
print(f'EXP0018 Phase00 validator: {len(errors)} errors, {len(warnings)} warnings')
for x in errors: print('ERROR:',x)
for x in warnings: print('WARN:',x)
sys.exit(1 if errors else 0)
