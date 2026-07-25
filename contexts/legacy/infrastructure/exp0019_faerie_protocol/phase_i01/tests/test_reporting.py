from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from fp_i01_compatibility.reporting import build_report,write_report
from fp_i01_compatibility.enums import CompatibilityStatus
ROOT=find_repository_root(__file__)

def test_report_is_pass_and_complete():
    r=build_report(ROOT)
    assert r.status is CompatibilityStatus.PASS
    assert len(r.dependency_results)==19 and len(r.adapter_results)==8 and len(r.previous_context_tests)==12
    assert not r.blockers and r.metaeditor_status=='pending_local_windows'

def test_report_hash_is_repeatable():
    assert build_report(ROOT).report_hash==build_report(ROOT).report_hash

def test_report_serializes_to_json():
    p=write_report(ROOT,build_report(ROOT));data=json.loads(p.read_text())
    assert data['status']=='PASS' and len(data['report_hash'])==64
