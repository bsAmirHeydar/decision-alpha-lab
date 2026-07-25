from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)

def test_phase_python_has_no_order_or_network_authority():
    text='\n'.join(
        p.read_text(errors='ignore')
        for p in (ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i05/python').rglob('*.py')
    ).lower()
    for forbidden in ('ordersend','positionopen','urllib','requests.','socket.'):
        assert forbidden not in text

def test_phase_does_not_modify_previous_phase_sources():
    assert (ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i04/python/fp_i04_data/synchronization.py').exists()
