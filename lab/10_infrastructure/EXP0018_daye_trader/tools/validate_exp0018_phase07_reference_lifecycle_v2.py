from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
CONTRACT=ROOT/'lab/10_infrastructure/EXP0018_daye_trader/contracts/daye_reference_lifecycle_contract_v2.json'
FIXTURES=ROOT/'lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_reference_lifecycle_cases_v2.csv'
EXPERT=ROOT/'mql5/Experts/DayeTrader/EXP0018_Daye_Reference_Lifecycle_Anatomy.mq5'
INCLUDE_DIR=ROOT/'mql5/Include/DayeTrader/EXP0018'

def fail(msg:str)->None:
    raise AssertionError(msg)

def main()->int:
    c=json.loads(CONTRACT.read_text(encoding='utf-8'))
    if c['phase']!='P07' or c['schema_version']!=2: fail('contract identity')
    if c['authority']['execution'] or c['authority']['drawing'] or c['authority']['direction_mapping']: fail('forbidden authority')
    required={
      'one exact opportunity may produce at most one accepted use',
      'a later distinct opportunity may reuse the same reference while the same protected symbol remains unhunted',
      'the protected symbol touching its own reference retires the reference side',
      'retired references never return to active state',
      'accepted historical uses remain immutable after retirement'
    }
    if not required.issubset(set(c['core_rules'])): fail('core rule missing')
    rows=list(csv.DictReader(FIXTURES.open(encoding='utf-8')))
    if len(rows)<14: fail('fixture count')
    ids=[r['case_id'] for r in rows]
    if len(ids)!=len(set(ids)): fail('duplicate fixture id')
    required_cases={'same_exact_opportunity_repeats','later_distinct_opportunity_same_protected','protected_touch','double_hunt','role_switch','retired_cannot_reenter'}
    if not required_cases.issubset(ids): fail('critical fixture missing')
    code='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in [EXPERT,*INCLUDE_DIR.glob('DAYE_Lifecycle*.mqh')])
    for token in ('OrderSend','CTrade','PositionOpen','WebRequest'):
        if token in code: fail(f'forbidden token {token}')
    for required_token in ('RETIRED_PROTECTED_TOUCH','DUPLICATE_EXACT_OPPORTUNITY','allow_repeat_across_new_opportunities_while_protected_survives','ExportSourceObservations'):
        if required_token not in code: fail(f'missing implementation token {required_token}')
    print('EXP0018 Phase 07 contract validation: PASS')
    print(f'fixtures: {len(rows)}')
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print(f'EXP0018 Phase 07 validation: FAIL: {exc}',file=sys.stderr)
        raise
