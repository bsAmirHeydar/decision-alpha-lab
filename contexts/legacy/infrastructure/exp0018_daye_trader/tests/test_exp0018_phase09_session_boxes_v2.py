from tools.repository_paths import find_repository_root
from pathlib import Path
import csv,json,subprocess,sys
INFRA=Path(__file__).resolve().parents[1]
REPO=find_repository_root(__file__)

def test_contract_boundaries():
    c=json.loads((INFRA/'contracts/daye_session_box_contract_v2.json').read_text(encoding='utf-8'))
    assert c['authority']['session_box_drawing'] is True
    assert c['authority']['execution'] is False
    assert c['sessions']['A']['ny']=='18:00-00:00'
    assert c['sessions']['P']['ny']=='12:00-17:00'
    assert c['ownership']['foreign_objects_untouched'] is True

def test_fixture_policies():
    rows={r['case_id']:r for r in csv.DictReader((INFRA/'fixtures/daye_session_box_cases_v2.csv').open(encoding='utf-8'))}
    assert rows['p_open_update']['expected']=='UPDATED_OPEN'
    assert rows['partial_default_skip']['expected']=='SKIPPED_INELIGIBLE_COMPLETENESS'
    assert rows['waiting_symbol_chart']['expected']=='WAITING_FOR_SYMBOL_CHART'
    assert rows['orphan_cleanup']['expected']=='ORPHAN_DELETED'

def test_static_validator():
    validator=INFRA/'tools/validate_exp0018_phase09_session_boxes_v2.py'
    result=subprocess.run([sys.executable,str(validator),str(REPO)],capture_output=True,text=True)
    assert result.returncode==0, result.stdout+result.stderr
