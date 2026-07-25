from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);files=sorted(list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_39').glob('*'))+list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_39').glob('*')));assert len(files)>=28
bad=['OrderSend(','CTrade','trade.Buy','trade.Sell','PositionOpen(','PositionClose(','WebRequest(','SocketCreate(']
for p in files:
 s=p.read_text(encoding='utf-8');assert 'SAEDV439' in s
 for t in bad:assert t not in s,(p,t)
print(f'SAED V4-39 MQL5 static: {len(files)} files passed; order/network APIs absent')
