from tools.repository_paths import find_repository_root
from pathlib import Path
def test_i13_upstream_package_present():
    root=Path(__file__).resolve().parents[2]/'phase_i13/python'
    assert (root/'fp_i13_release/__init__.py').exists()
def test_i13_release_entrypoints_present():
    root=find_repository_root(__file__)
    assert (root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5').exists()
