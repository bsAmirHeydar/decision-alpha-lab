#!/usr/bin/env python3
from __future__ import annotations
import csv, json, sys
from pathlib import Path

VALID_COMPLETENESS={"EMPTY","OPEN","PARTIAL","COMPLETE","UNAVAILABLE","INVALID"}

def classify(row):
    start=int(row['start_utc']); end=int(row['end_utc']); base=int(row['base_seconds'])
    observed=int(row['observed_bars']); now=int(row['now_utc'])
    first_off=int(row['first_bar_offset_seconds']); last_off=int(row['last_bar_offset_seconds'])
    elapsed=end-start
    if base<=0 or elapsed<=0 or elapsed%base: return 'INVALID',0
    expected=elapsed//base
    if observed==0: return 'EMPTY',expected
    if now<end: return 'OPEN',expected
    exact=(observed==expected and first_off==0 and last_off==elapsed-base)
    return ('COMPLETE' if exact else 'PARTIAL'),expected

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    cpath=root/'contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_period_aggregation_contract_v2.json'
    fpath=root/'contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_period_aggregation_cases_v2.csv'
    errors=[]
    contract=json.loads(cpath.read_text(encoding='utf-8'))
    if contract.get('execution_authority') is not False: errors.append('execution_authority_must_be_false')
    if contract.get('p4_minutes') != 30: errors.append('p4_must_be_30_minutes')
    if contract.get('weekly_status') != 'blocked_until_ADR-DY-A03': errors.append('weekly_must_remain_blocked')
    if set(contract.get('completeness',[])) != VALID_COMPLETENESS: errors.append('completeness_enum_mismatch')
    rows=list(csv.DictReader(fpath.open(encoding='utf-8')))
    if len(rows)<8: errors.append('insufficient_fixture_rows')
    for row in rows:
        actual,expected=classify(row)
        if actual!=row['expected_completeness']: errors.append(f"{row['case_id']}: completeness {actual} != {row['expected_completeness']}")
        if expected!=int(row['expected_bars']): errors.append(f"{row['case_id']}: expected bars {expected} != {row['expected_bars']}")
    if errors:
        print('EXP0018 P03 validator: FAIL')
        for e in errors: print('ERROR',e)
        return 1
    print('EXP0018 P03 validator: PASS')
    print(f'fixtures={len(rows)} p4_minutes=30 weekly=blocked execution_authority=false')
    return 0
if __name__=='__main__': raise SystemExit(main())
