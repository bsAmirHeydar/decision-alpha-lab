from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_mql5_mirror_is_diagnostic_only():
 files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4OutcomeCube').glob('*.mqh'));assert len(files)>=12
 text='\n'.join(p.read_text() for p in files);assert 'OrderSend' not in text;assert 'WebRequest' not in text;assert 'PRODUCTION_AUTHORIZATION false' in text
