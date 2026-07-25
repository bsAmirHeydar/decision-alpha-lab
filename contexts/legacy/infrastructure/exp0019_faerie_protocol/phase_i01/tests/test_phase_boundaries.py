from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)

def test_no_indicator_or_execution_product_is_created_in_i01():
    owned=[ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01',ROOT/'mql5/Include/FaerieProtocol/EXP0019/Compatibility',ROOT/'mql5/Experts/FaerieProtocol',ROOT/'mql5/Tests/Experts/FaerieProtocol']
    files=[p for base in owned for p in base.rglob('*') if p.is_file()]
    names='\n'.join(p.name.lower() for p in files)
    assert '.mq4' not in names
    assert not any(p.suffix=='.mq5' and 'indicator' in p.name.lower() for p in files)

def test_open_decision_012_is_not_inferred():
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in (ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01').rglob('*') if p.is_file())
    assert 'FP-DEC-012' not in text or 'open' in text.lower()
