from __future__ import annotations
import csv,json,re,sys
from pathlib import Path

root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
base=root/'lab/10_infrastructure/EXP0018_daye_trader'
contract=json.loads((base/'contracts/daye_close_confirmation_contract_v2.json').read_text(encoding='utf-8'))
rows=list(csv.DictReader((base/'fixtures/daye_close_confirmation_cases_v2.csv').open(encoding='utf-8')))
errors=[]

def expected(row):
    if row['missed_close']=='1': return 'MISSED_CLOSE_REPLAY_REQUIRED'
    if row['host_identity_match']!='1': return 'UNAVAILABLE_AT_CLOSE'
    if row['source_available_through_close']!='1': return 'UNAVAILABLE_AT_CLOSE'
    close=row['close_pair']; initial=row['initial_pair']
    if close=='BOTH': return 'INVALIDATED_DOUBLE_HUNT'
    if close=='NONE': return 'NO_SIGNAL_AT_CLOSE'
    if close in ('UNAVAILABLE','UNKNOWN'): return 'UNAVAILABLE_AT_CLOSE'
    if close!=initial: return 'INVALIDATED_ROLE_CHANGED'
    return 'CONFIRMED'

if contract.get('execution_authority') is not False: errors.append('execution authority must be false')
if contract.get('drawing_authority') is not False: errors.append('drawing authority must be false')
if contract.get('reference_lifecycle_authority') is not False: errors.append('lifecycle authority must be false')
if len(contract.get('outcomes',[]))!=6: errors.append('exactly six outcomes required')
if len(contract.get('invariants',[]))<10: errors.append('at least ten invariants required')
if len(rows)<12: errors.append('at least twelve golden fixtures required')
for row in rows:
    actual=expected(row)
    if actual!=row['expected_outcome']: errors.append(f"fixture {row['case_id']} expected {row['expected_outcome']} got {actual}")
    confirmed='1' if actual=='CONFIRMED' else '0'
    if confirmed!=row['expected_confirmed']: errors.append(f"fixture {row['case_id']} confirmed mismatch")

required=[
 'mql5/Experts/DayeTrader/EXP0018_Daye_Close_Confirmation_Anatomy.mq5',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationTypes.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_HostCloseClock.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationStateMachine.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationStore.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationCheckpoint.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationEvents.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationDiagnostics.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationAudit.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationSelfTest.mqh',
 'mql5/Include/DayeTrader/EXP0018/DAYE_ConfirmationEngine.mqh',
]
for rel in required:
    if not (root/rel).exists(): errors.append('missing '+rel)

for rel in required:
    path=root/rel
    if not path.exists(): continue
    text=path.read_text(encoding='utf-8')
    if text.count('{')!=text.count('}'): errors.append('brace mismatch '+rel)
    for token in ('OrderSend','CTrade','PositionOpen','WebRequest','ObjectCreate('):
        if token in text: errors.append(f'forbidden token {token} in {rel}')
    if 'LongToString(' in text: errors.append('LongToString compatibility risk '+rel)

expert=(root/required[0]).read_text(encoding='utf-8') if (root/required[0]).exists() else ''
for token in ('InpHostTimeframe','InpPersistCheckpoint','InpRequireExactHostSymbolAlignment','InpPublishNonconfirmedResults'):
    if token not in expert: errors.append('missing expert input '+token)

if errors:
    print('EXP0018 Phase 06 validation: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('EXP0018 Phase 06 validation: PASS')
print('fixtures',len(rows))
print('outcomes',len(contract['outcomes']))
print('invariants',len(contract['invariants']))
