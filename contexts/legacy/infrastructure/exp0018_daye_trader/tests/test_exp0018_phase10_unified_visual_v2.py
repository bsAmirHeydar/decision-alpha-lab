from tools.repository_paths import find_repository_root
from pathlib import Path
import csv, json
INFRA=Path(__file__).resolve().parents[1]
REPO=find_repository_root(__file__)

def test_contract_core_layers():
    c=json.loads((INFRA/'contracts/daye_unified_visual_contract_v2.json').read_text())
    assert c['execution_authority'] is False
    assert c['micro_quarter_seconds']==1350
    assert c['p4_duration_minutes']==30
    assert c['ww_activation'] is False

def test_fixtures_cover_required_cases():
    rows=list(csv.DictReader((INFRA/'fixtures/daye_unified_visual_cases_v2.csv').open()))
    ids={r['case_id'] for r in rows}
    assert {'p4_tail','gap','tdo','two_literal','manual_move','foreign_object'} <= ids

def test_visual_code_boundaries():
    text=(REPO/'mql5/Include/DayeTrader/EXP0018/DAYE_VisualEngine.mqh').read_text()
    assert 'q*1350' in text
    assert 'DAYE_FAMILY_SUBCYCLE_90M' in text
    assert 'DAYE_FAMILY_SUBCYCLE_TAIL' in text
    assert 'render_provisional_week_boundaries' in text

def test_no_execution_authority():
    text=''.join(p.read_text() for p in (REPO/'mql5/Include/DayeTrader/EXP0018').glob('DAYE_Visual*.mqh'))
    for token in ['OrderSend','CTrade','PositionOpen','WebRequest']:
        assert token not in text
