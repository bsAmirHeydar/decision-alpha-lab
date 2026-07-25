from pathlib import Path
import csv, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def test_contract_authority():
    c=json.loads((ROOT/'contracts/daye_divergence_drawing_contract_v2.json').read_text(encoding='utf-8'))
    assert c['authority']['drawing'] is True
    assert c['authority']['execution'] is False
    assert c['persistence']['retirement_does_not_delete_historical_line'] is True

def test_fixture_semantics():
    rows=list(csv.DictReader((ROOT/'fixtures/daye_divergence_drawing_cases_v2.csv').open(encoding='utf-8')))
    by={r['case_id']:r for r in rows}
    assert by['major_high_create']['label_expected']=='1'
    assert by['minor_high_create']['label_expected']=='0'
    assert by['waiting_chart']['expected_status']=='WAITING_FOR_HUNTER_CHART'
    assert by['retired_reference_historical_line_preserved']['expected_status']=='VERIFIED'

def test_static_validator():
    validator=ROOT/'tools/validate_exp0018_phase08_divergence_drawing_v2.py'
    repo=ROOT.parents[2]
    result=subprocess.run([sys.executable,str(validator),str(repo)],capture_output=True,text=True)
    assert result.returncode==0, result.stdout+result.stderr
