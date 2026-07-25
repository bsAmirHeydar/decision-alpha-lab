from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);files=list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_13').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_13').glob('*.mq5'));assert len(files)==12
for p in files:
 t=p.read_text();assert '#pragma once' in t or '#property strict' in t;assert 'OrderSend' not in t and 'CTrade' not in t and 'WebRequest' not in t
print(f'validated {len(files)} SAED V4-13 MQL5 static reference files')
