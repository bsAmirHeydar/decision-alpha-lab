from __future__ import annotations
from pathlib import Path
import csv, json, re, sys

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
errors=[]

def req(rel):
    p=ROOT/rel
    if not p.exists(): errors.append(f"missing:{rel}")
    return p

contract_path=req('contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_unified_visual_contract_v2.json')
fixture_path=req('contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_unified_visual_cases_v2.csv')
expert_path=req('mql5/Experts/DayeTrader/EXP0018_Daye_Visual_Anatomy.mq5')
engine_path=req('mql5/Include/DayeTrader/EXP0018/DAYE_VisualEngine.mqh')
render_path=req('mql5/Include/DayeTrader/EXP0018/DAYE_RenderEngine.mqh')
for rel in [
'mql5/Include/DayeTrader/EXP0018/DAYE_VisualTypes.mqh',
'mql5/Include/DayeTrader/EXP0018/DAYE_VisualIdentity.mqh',
'mql5/Include/DayeTrader/EXP0018/DAYE_VisualObjectManager.mqh',
'mql5/Include/DayeTrader/EXP0018/DAYE_VisualSelfTest.mqh',
'docs/history/obsidian/deep/00_mocs/CG_EXP0018_PHASE10_UNIFIED_VISUAL_ANATOMY_MOC.md']:
    req(rel)

if contract_path.exists():
    c=json.loads(contract_path.read_text(encoding='utf-8'))
    if c.get('execution_authority') is not False: errors.append('execution_authority_not_false')
    if c.get('micro_quarter_seconds')!=1350: errors.append('micro_quarter_not_1350')
    if c.get('p4_duration_minutes')!=30: errors.append('p4_not_30')
    if c.get('ww_activation') is not False: errors.append('ww_must_remain_blocked')
    required={'divergence','daily_frame','session_boxes','subcycle_boxes','micro_22_5_boundaries','gap_band','TDO','TWO'}
    if not required.issubset(set(c.get('default_on_layers',[]))): errors.append('required_default_layers_missing')

if fixture_path.exists():
    rows=list(csv.DictReader(fixture_path.open(encoding='utf-8')))
    if len(rows)<25: errors.append('fixture_count_below_25')
    ids={r['case_id'] for r in rows}
    for x in ['p4_tail','micro_q2_boundary','gap','tdo','two_literal','symbol_scale','foreign_object']:
        if x not in ids: errors.append(f'missing_fixture:{x}')

all_code=''
for p in list((ROOT/'mql5/Experts/DayeTrader').glob('EXP0018_Daye_Visual_Anatomy.mq5'))+list((ROOT/'mql5/Include/DayeTrader/EXP0018').glob('DAYE_Visual*.mqh')):
    text=p.read_text(encoding='utf-8')
    all_code+='\n'+text
    if text.count('{')!=text.count('}'): errors.append(f'brace_imbalance:{p.relative_to(ROOT)}')
for token in ['OrderSend','CTrade','PositionOpen','WebRequest']:
    if token in all_code: errors.append(f'forbidden_token:{token}')
for token in ['1350','DAYE_FAMILY_SUBCYCLE_TAIL','render_tdo','render_two','EXP0018_P10_','DAYE_DeleteOwnedVisualObjectsFromAllCharts']:
    if token not in all_code: errors.append(f'missing_code_contract:{token}')
if render_path.exists():
    rt=render_path.read_text(encoding='utf-8')
    if 'int ExportSourcePeriods(DAYE_PairedPeriodSnapshot &items[])' not in rt: errors.append('missing_render_source_export')
if expert_path.exists():
    et=expert_path.read_text(encoding='utf-8')
    for token in ['InpRenderMicro225Boundaries=true','InpRenderTDO=true','InpRenderTWO=true','InpRenderExtendedSessionTrueOpens=false','InpRenderProvisionalWeekBoundaries=false']:
        if token not in et: errors.append(f'expert_default_missing:{token}')

phase_dir=ROOT/'docs/operations/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2/17_phase10_unified_visual_anatomy_v2'
if not phase_dir.exists() or len(list(phase_dir.glob('*.md')))<35: errors.append('phase_docs_below_35')

if errors:
    print('EXP0018 P10 validation: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('EXP0018 P10 validation: PASS')
print('fixtures:', len(rows) if fixture_path.exists() else 0)
print('docs:', len(list(phase_dir.glob('*.md'))) if phase_dir.exists() else 0)
