from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];files=list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_16').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_16').glob('*.mq5'));assert files
for p in files:
 t=p.read_text(encoding='utf-8');assert 'SAED_V4_16' in t or 'SAEDV416' in t,p
 for banned in ['WebRequest(','OrderSend(','trade.Buy(','trade.Sell(','CTrade ']:assert banned not in t,(p,banned)
print(f'SAED V4-16 MQL5 static validation passed: {len(files)} files')
