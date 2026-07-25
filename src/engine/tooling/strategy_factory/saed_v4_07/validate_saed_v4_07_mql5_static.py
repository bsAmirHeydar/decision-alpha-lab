from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);I=ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4ActionLattice';E=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics';files=sorted(I.glob('*.mqh'))+sorted(E.glob('EXP_SAED_V4_07_*.mq5'))
if len(files)<16:raise SystemExit(f'insufficient MQL5 mirror: {len(files)}')
forbidden=('OrderSend(','OrderSendAsync(','CTrade','WebRequest(','SocketCreate(','#import')
errors=[]
for p in files:
 t=p.read_text()
 for token in forbidden:
  if token in t:errors.append(f'{p}:{token}')
 if p.suffix=='.mqh' and '#ifndef' not in t:errors.append(f'{p}:missing guard')
if errors:raise SystemExit('; '.join(errors))
print(f'validated {len(files)} diagnostic-only MQL5 files')
