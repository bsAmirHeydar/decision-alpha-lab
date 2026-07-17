from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];files=sorted(list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_41').glob('*'))+list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_41').glob('*')));assert len(files)>=32
bad=['OrderSend(','CTrade','trade.Buy','trade.Sell','PositionOpen(','PositionClose(','WebRequest(','SocketCreate(']
for p in files:
 s=p.read_text(encoding='utf-8');assert 'SAEDV441' in s
 for t in bad:assert t not in s,(p,t)
print(f'SAED V4-41 MQL5 static: {len(files)} files passed; order/network APIs absent')
