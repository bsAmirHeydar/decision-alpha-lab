from tools.repository_paths import find_repository_root
from pathlib import Path
from fp_i01_compatibility.duplicate_scan import scan_paths
ROOT=find_repository_root(__file__)

def test_phase_owned_code_contains_no_duplicate_core_or_runtime_authority():
    findings=scan_paths(ROOT,['contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01','mql5/Include/FaerieProtocol/EXP0019/Compatibility','mql5/Experts/FaerieProtocol','mql5/Tests/Experts/FaerieProtocol'])
    assert findings==()

def test_scan_detects_forbidden_authority_in_temp_tree(tmp_path):
    p=tmp_path/'x.py';p.write_text('OrderSend(1)')
    findings=scan_paths(tmp_path,['.'])
    assert any(x['code']=='ORDER_AUTHORITY' for x in findings)
