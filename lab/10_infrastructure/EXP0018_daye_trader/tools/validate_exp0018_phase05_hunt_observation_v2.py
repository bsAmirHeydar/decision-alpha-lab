from __future__ import annotations
import csv, json, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv)>1 else '.')
contract_path = root/'lab/10_infrastructure/EXP0018_daye_trader/contracts/daye_hunt_observation_contract_v2.json'
fixture_path = root/'lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_hunt_observation_cases_v2.csv'
expert_path = root/'mql5/Experts/DayeTrader/EXP0018_Daye_Hunt_Observation_Anatomy.mq5'
errors=[]

contract=json.loads(contract_path.read_text(encoding='utf-8'))
if contract.get('execution_authority') is not False: errors.append('execution_authority must be false')
if contract.get('direction_authority') is not False: errors.append('direction_authority must be false')
if contract['core_rules'].get('equality_counts') is not True: errors.append('equality must count')
if contract['core_rules'].get('first_touch_time_claimed') is not False: errors.append('P05 must not claim exact first touch time')

rows=list(csv.DictReader(fixture_path.open(encoding='utf-8')))
if len(rows) < 10: errors.append('fixture catalog too small')

def classify(row):
    side=row['side']
    if side=='HIGH':
        a=float(row['a_current_high']) >= float(row['a_ref_high'])
        b=float(row['b_current_high']) >= float(row['b_ref_high'])
        ae=float(row['a_current_high']) == float(row['a_ref_high'])
        be=float(row['b_current_high']) == float(row['b_ref_high'])
    else:
        a=float(row['a_current_low']) <= float(row['a_ref_low'])
        b=float(row['b_current_low']) <= float(row['b_ref_low'])
        ae=float(row['a_current_low']) == float(row['a_ref_low'])
        be=float(row['b_current_low']) == float(row['b_ref_low'])
    state='BOTH' if a and b else 'A_ONLY' if a else 'B_ONLY' if b else 'NONE'
    return state,a,b,ae,be

for row in rows:
    state,a,b,ae,be=classify(row)
    expected=(row['expected_pair_state'],row['expected_a_hunted']=='1',row['expected_b_hunted']=='1',row['expected_a_equality']=='1',row['expected_b_equality']=='1')
    actual=(state,a,b,ae,be)
    if actual != expected: errors.append(f"fixture {row['case_id']} expected {expected} got {actual}")

text='\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in [expert_path] + list((root/'mql5/Include/DayeTrader/EXP0018').glob('DAYE_Hunt*.mqh')))
for token in contract['forbidden_tokens']:
    if token in text: errors.append(f'forbidden token present: {token}')
for required in ['current_extreme >= fact.reference_price','current_extreme <= fact.reference_price']:
    pass

if errors:
    print('EXP0018 P05 validation: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('EXP0018 P05 validation: PASS')
print('fixtures:',len(rows))
