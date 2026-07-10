from pathlib import Path
import csv,json,re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
errors=[]
required=[
'mql5/Experts/DayeTrader/EXP0018_Daye_Historical_Replay_Anatomy.mq5',
'mql5/Include/DayeTrader/EXP0018/DAYE_ReplayTypes.mqh',
'mql5/Include/DayeTrader/EXP0018/DAYE_ReplayDataLoader.mqh',
'mql5/Include/DayeTrader/EXP0018/DAYE_ReplayReducer.mqh',
'mql5/Include/DayeTrader/EXP0018/DAYE_ReplayEngine.mqh',
'lab/10_infrastructure/EXP0018_daye_trader/contracts/daye_historical_replay_contract_v2.json']
for x in required:
    if not (root/x).exists(): errors.append('missing:'+x)
contract=json.loads((root/required[-1]).read_text())
if contract.get('execution_authority') is not False: errors.append('execution_authority_must_be_false')
expert=(root/required[0]).read_text()
all_mql='\n'.join(p.read_text(errors='ignore') for p in [root/x for x in required[:5]])
for token in contract['forbidden_capabilities']:
    if re.search(r'\b'+re.escape(token)+r'\b',all_mql): errors.append('forbidden:'+token)
for marker in ['InpReplayStartNewYork','InpRequireCompleteSourceAlignment','CDayeHistoricalReplayEngine','ProcessChunk']:
    if marker not in expert and marker not in all_mql: errors.append('missing_marker:'+marker)
with (root/'lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_historical_replay_cases_v2.csv').open() as f:
    rows=list(csv.DictReader(f))
if len(rows)<18: errors.append('fixture_count_below_18')
for marker in ['DAYE_AggregateSymbolBars','DAYE_ResolveRelationshipOpportunities','DAYE_ClassifyHuntObservations','DAYE_FinalizeCandidateAtClose','DAYE_ApplyObservationToReference']:
    if marker not in all_mql: errors.append('pure_pipeline_marker_missing:'+marker)
print('EXP0018 P11 validator:', 'PASS' if not errors else 'FAIL')
for e in errors: print(' -',e)
raise SystemExit(1 if errors else 0)
