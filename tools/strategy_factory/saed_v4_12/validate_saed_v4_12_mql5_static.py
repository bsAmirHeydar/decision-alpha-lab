from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];files=list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_12').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_12').glob('*.mq5'));assert files
for p in files:
 t=p.read_text(encoding='utf-8');low=t.lower();assert '#property strict' in low or p.suffix=='.mqh';assert 'saed_v4_12' in low
 for forbidden in ['ordersend','ctrade','trade.mqh','positionopen','buy(','sell(']:assert forbidden not in low,(p,forbidden)
print(f'V4-12 MQL5 static validation passed: {len(files)} files')
