from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
BASE=ROOT/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I05'

def test_mql5_catalog_and_all_header_exist():
    assert (BASE/'FP_I05_All.mqh').exists()
    assert 'return 12;' in (BASE/'FP_I05_Registry.mqh').read_text()

def test_mql5_reference_policy_is_hunter_nonconsuming_protected_consuming():
    text=(BASE/'FP_I05_ReferenceEngine.mqh').read_text()
    assert 'FP_I05_REF_HUNTER_SEEN' in text
    assert 'FP_I05_REF_CONSUMED_BY_PROTECTED' in text

def test_mql5_phase_has_no_order_authority():
    text='\n'.join(p.read_text(errors='ignore').lower() for p in BASE.rglob('*.mqh'))
    assert 'ordersend' not in text and 'positionopen' not in text and 'ctrade' not in text
