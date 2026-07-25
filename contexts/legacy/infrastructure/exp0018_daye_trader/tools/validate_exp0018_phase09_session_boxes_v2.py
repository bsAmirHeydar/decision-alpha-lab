from pathlib import Path
import json,csv,re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
errors=[]
contract=json.loads((root/'contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_session_box_contract_v2.json').read_text(encoding='utf-8'))
if contract['phase']!='P09': errors.append('phase must be P09')
if contract['authority']['execution'] or contract['authority']['risk'] or contract['authority']['signal']: errors.append('forbidden authority enabled')
if contract['object_prefix']!='EXP0018_P09_BOX_': errors.append('object prefix mismatch')
if set(contract['sessions'])!={'A','L','N','P'}: errors.append('session set mismatch')
if contract['geometry']['object_type']!='OBJ_RECTANGLE': errors.append('object type mismatch')
if contract['admission_defaults']['partial'] is not False: errors.append('partial default must be false')
rows=list(csv.DictReader((root/'contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_session_box_cases_v2.csv').open(encoding='utf-8')))
expected={'a_complete_create','l_complete_verify','n_complete_repair','p_open_update','partial_default_skip','empty_skip','disabled_session_skip','outside_lookback_skip','waiting_symbol_chart','manual_delete_recreate','orphan_cleanup','symbol_local_scale'}
ids={r['case_id'] for r in rows}
if ids!=expected: errors.append(f'fixture mismatch missing={expected-ids} extra={ids-expected}')
include_dir=root/'mql5/Include/DayeTrader/EXP0018'
expert=root/'mql5/Experts/DayeTrader/EXP0018_Daye_Session_Boxes_Anatomy.mq5'
required=['DAYE_SessionBoxTypes.mqh','DAYE_SessionBoxIdentity.mqh','DAYE_SessionBoxPolicy.mqh','DAYE_SessionBoxGeometry.mqh','DAYE_SessionBoxChartResolver.mqh','DAYE_SessionBoxObjectManager.mqh','DAYE_SessionBoxStore.mqh','DAYE_SessionBoxEvents.mqh','DAYE_SessionBoxDiagnostics.mqh','DAYE_SessionBoxAudit.mqh','DAYE_SessionBoxSelfTest.mqh','DAYE_SessionBoxEngine.mqh']
for name in required:
    if not (include_dir/name).exists(): errors.append('missing '+name)
if not expert.exists(): errors.append('missing P09 expert')
source='\n'.join(p.read_text(encoding='utf-8') for p in list(include_dir.glob('DAYE_SessionBox*.mqh'))+[expert])
for token in ['OrderSend','CTrade','PositionOpen','WebRequest','EXP0017']:
    if token in source: errors.append('forbidden token '+token)
for token in ['OBJ_RECTANGLE','OBJPROP_FILL','DAYE_SESSION_BOX_OBJECT_PREFIX','DAYE_FAMILY_SESSION','DAYE_SESSION_BOX_TARGET_ALL_OPEN_SYMBOL_CHARTS','ColorToARGB','DeleteOrphanedSessionBoxes']:
    if token not in source: errors.append('missing implementation token '+token)
if 'symbol_a.high' not in (include_dir/'DAYE_SessionBoxEngine.mqh').read_text(encoding='utf-8') and 'snapshot.high' not in source:
    errors.append('symbol-local range evidence missing')
# Basic brace balance, excluding comments/strings is not attempted; gross mismatch only.
for p in list(include_dir.glob('DAYE_SessionBox*.mqh'))+[expert]:
    t=p.read_text(encoding='utf-8')
    if t.count('{')!=t.count('}'): errors.append('brace mismatch '+p.name)
print('EXP0018 P09 validator:', 'PASS' if not errors else 'FAIL')
for e in errors: print('ERROR:',e)
sys.exit(1 if errors else 0)
