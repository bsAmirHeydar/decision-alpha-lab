from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);files=list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_10').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_10').glob('*.mq5'))
for p in files:
 t=p.read_text(errors='ignore');assert '#ifndef' in t or '#property strict' in t;assert 'OrderSend(' not in t;assert 'CTrade' not in t
print(f'{len(files)} MQL5 files passed static validation; MetaEditor compile remains pending_local_windows')
