from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];folders=[ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_23',ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_23'];files=[p for f in folders for p in f.glob('*') if p.suffix in {'.mqh','.mq5'}]
assert len(files)>=20
for p in files:
    t=p.read_text(encoding='utf-8');assert 'SAED_V4_23' in t and '#property strict' in t
    for forbidden in ['OrderSend(','trade.Buy(','trade.Sell(','PositionOpen(','WebRequest(']:assert forbidden not in t,p
print(f'V4-23 MQL5 static validation passed: {len(files)} files; MetaEditor pending_local_windows')
