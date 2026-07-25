from tools.repository_paths import find_repository_root
import csv, json
from pathlib import Path

ROOT=find_repository_root(__file__)

def test_contract_authority_and_rules():
    c=json.loads((ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_reference_lifecycle_contract_v2.json').read_text())
    assert c['authority']['reference_lifecycle'] is True
    assert c['authority']['execution'] is False
    assert c['authority']['drawing'] is False
    assert 'retired references never return to active state' in c['core_rules']

def test_fixture_transition_coverage():
    rows=list(csv.DictReader((ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_reference_lifecycle_cases_v2.csv').open()))
    by_id={r['case_id']:r for r in rows}
    assert by_id['same_exact_opportunity_repeats']['expected_use_status']=='DUPLICATE_EXACT_OPPORTUNITY'
    assert by_id['later_distinct_opportunity_same_protected']['expected_use_status']=='ACCEPTED'
    assert by_id['protected_touch']['expected_state']=='RETIRED_PROTECTED_TOUCH'
    assert by_id['double_hunt']['expected_state']=='RETIRED_DOUBLE_HUNT'
    assert by_id['role_switch']['expected_state']=='RETIRED_ROLE_SWITCH'

def test_high_low_and_reference_identity_are_independent():
    rows=list(csv.DictReader((ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_reference_lifecycle_cases_v2.csv').open()))
    ids={r['case_id'] for r in rows}
    assert 'high_low_independent' in ids
    assert 'different_reference_period' in ids

def test_no_execution_or_drawing_authority():
    code='\n'.join(p.read_text(errors='ignore') for p in [ROOT/'mql5/Experts/DayeTrader/EXP0018_Daye_Reference_Lifecycle_Anatomy.mq5',*(ROOT/'mql5/Include/DayeTrader/EXP0018').glob('DAYE_Lifecycle*.mqh')])
    for token in ('OrderSend','CTrade','PositionOpen','WebRequest','ObjectCreate'):
        assert token not in code
