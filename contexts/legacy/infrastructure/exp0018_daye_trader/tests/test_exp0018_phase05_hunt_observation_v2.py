from tools.repository_paths import find_repository_root
from pathlib import Path
import csv, json, subprocess, sys

ROOT=find_repository_root(__file__)

def test_validator_passes():
    script=ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase05_hunt_observation_v2.py'
    result=subprocess.run([sys.executable,str(script),str(ROOT)],capture_output=True,text=True)
    assert result.returncode==0, result.stdout+result.stderr

def test_contract_boundaries():
    c=json.loads((ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_hunt_observation_contract_v2.json').read_text())
    assert c['execution_authority'] is False
    assert c['direction_authority'] is False
    assert c['confirmation_authority'] is False
    assert c['core_rules']['first_touch_time_claimed'] is False

def test_equality_fixtures_exist():
    rows=list(csv.DictReader((ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_hunt_observation_cases_v2.csv').open()))
    ids={r['case_id'] for r in rows}
    assert 'high_equality_a' in ids
    assert 'low_equality_b' in ids

def test_no_forward_or_cross_scale_semantics():
    text=(ROOT/'mql5/Include/DayeTrader/EXP0018/DAYE_HuntClassifier.mqh').read_text()
    assert 'resolution.current_period.symbol_a' in text
    assert 'resolution.reference_period.symbol_a' in text
    assert 'resolution.current_period.symbol_b' in text
    assert 'resolution.reference_period.symbol_b' in text
    assert 'nearest' not in text.lower()
