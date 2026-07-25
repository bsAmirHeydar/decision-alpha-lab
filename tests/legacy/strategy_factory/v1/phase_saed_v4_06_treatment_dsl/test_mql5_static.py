from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_mql5_mirror_is_diagnostic_only():
 files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4TreatmentDsl').glob('*.mqh'))+list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_06_*.mq5'))
 assert len(files)>=13
 for p in files:
  t=p.read_text();assert 'OrderSend(' not in t;assert 'WebRequest(' not in t;assert 'CTrade' not in t
