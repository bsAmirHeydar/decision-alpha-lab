from tools.repository_paths import find_repository_root
from pathlib import Path
def test_no_broker_authority():
 root=find_repository_root(__file__)
 paths=[root/'mql5/Include/AlphaLab/StrategyFactory/TreatmentCompiler',root/'src/engine/packages/strategy_factory_treatment_compiler_v3']
 banned=('OrderSend(','OrderCheck(','CTrade','PositionOpen(','requests.','socket.')
 for p in paths:
  for f in p.rglob('*'):
   if f.is_file() and f.suffix in ('.py','.mqh','.mq5'):
    text=f.read_text(encoding='utf-8',errors='ignore')
    assert not any(x in text for x in banned),(f,banned)
