from pathlib import Path
import json, csv, re, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
errors=[]
contract_path=root/'lab/10_infrastructure/EXP0018_daye_trader/contracts/daye_divergence_drawing_contract_v2.json'
fixture_path=root/'lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_divergence_drawing_cases_v2.csv'
contract=json.loads(contract_path.read_text(encoding='utf-8'))
if contract['phase']!='P08': errors.append('phase must be P08')
if contract['authority']['execution'] or contract['authority']['risk'] or contract['authority']['direction']: errors.append('forbidden authority enabled')
if contract['object_prefix']!='EXP0018_P08_': errors.append('object prefix mismatch')
if contract['labels']['major_count']!=6 or contract['labels']['minor_count']!=16: errors.append('label cardinality mismatch')
if not contract['persistence']['confirmed_line_immutable']: errors.append('confirmed line must be immutable')
with fixture_path.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
expected={'major_high_create','major_low_create','minor_high_create','existing_exact_verify','existing_mismatch_repair','waiting_chart','missing_reference_period','missing_extreme_time','rejected_use_skipped','retired_reference_historical_line_preserved','simultaneous_major_minor_independent'}
ids={r['case_id'] for r in rows}
if ids!=expected: errors.append(f'fixture set mismatch missing={expected-ids} extra={ids-expected}')

include_dir=root/'mql5/Include/DayeTrader/EXP0018'
expert=root/'mql5/Experts/DayeTrader/EXP0018_Daye_Divergence_Drawing_Anatomy.mq5'
required=['DAYE_RenderTypes.mqh','DAYE_RenderIdentity.mqh','DAYE_RenderProjection.mqh','DAYE_RenderChartResolver.mqh','DAYE_RenderObjectManager.mqh','DAYE_RenderStore.mqh','DAYE_RenderEvents.mqh','DAYE_RenderDiagnostics.mqh','DAYE_RenderAudit.mqh','DAYE_RenderSelfTest.mqh','DAYE_RenderEngine.mqh']
for name in required:
    if not (include_dir/name).exists(): errors.append('missing '+name)
if not expert.exists(): errors.append('missing P08 expert')
source='\n'.join(p.read_text(encoding='utf-8') for p in list(include_dir.glob('DAYE_Render*.mqh'))+[expert])
for token in ['OrderSend','CTrade','PositionOpen','WebRequest']:
    if token in source: errors.append('forbidden token '+token)
for required_token in ['OBJ_TREND','DAYE_RENDER_OBJECT_PREFIX','DAYE_RENDER_TARGET_ALL_OPEN_HUNTER_CHARTS','DAYE_EXTREME_ANCHOR_FIRST_OCCURRENCE','ObjectCreate','ChartFirst','ChartNext']:
    if required_token not in source: errors.append('missing implementation token '+required_token)
if 'EXP0017' in source: errors.append('EXP0017 dependency forbidden')
p07=(root/'mql5/Experts/DayeTrader/EXP0018_Daye_Reference_Lifecycle_Anatomy.mq5').read_text(encoding='utf-8')
if re.search(r'\bc\.(hunt_config|require_exact_host_symbol_alignment|persist_checkpoint|publish_nonconfirmed_results|maximum_results_to_publish)',p07): errors.append('stray config alias c detected in P07 expert')

p03=(include_dir/'DAYE_PeriodTypes.mqh').read_text(encoding='utf-8')
for field in ['high_first_time_utc','high_last_time_utc','low_first_time_utc','low_last_time_utc']:
    if field not in p03: errors.append('missing P03 extreme provenance '+field)
for api_file in ['DAYE_RelationshipEngine.mqh','DAYE_HuntEngine.mqh','DAYE_ConfirmationEngine.mqh','DAYE_LifecycleEngine.mqh']:
    if 'ExportSourcePeriods' not in (include_dir/api_file).read_text(encoding='utf-8'): errors.append('missing read-only source period API in '+api_file)

print('EXP0018 P08 validator:', 'PASS' if not errors else 'FAIL')
for e in errors: print('ERROR:',e)
sys.exit(1 if errors else 0)
