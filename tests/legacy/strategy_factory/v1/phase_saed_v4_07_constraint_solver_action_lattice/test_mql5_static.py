from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_mql5_is_diagnostic_only():
 files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4ActionLattice').glob('*.mqh'))+list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_07_*.mq5'));assert len(files)>=16
 for p in files:
  t=p.read_text();assert 'OrderSend(' not in t and 'CTrade' not in t and 'WebRequest(' not in t
