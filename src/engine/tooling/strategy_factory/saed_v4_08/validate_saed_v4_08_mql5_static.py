from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);files=sorted((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4OutcomeCube').glob('*.mqh'))+sorted((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_08_*.mq5'))
if len(files)<15:raise SystemExit('insufficient MQL5 mirror files')
for p in files:
 t=p.read_text()
 for bad in ('OrderSend(','WebRequest(','CTrade','PositionOpen('):
  if bad in t:raise SystemExit(f'prohibited runtime token {bad}: {p}')
 if p.suffix=='.mqh' and '#ifndef' not in t:raise SystemExit(f'missing include guard: {p}')
print(f'{len(files)} MQL5 files passed static validation')
