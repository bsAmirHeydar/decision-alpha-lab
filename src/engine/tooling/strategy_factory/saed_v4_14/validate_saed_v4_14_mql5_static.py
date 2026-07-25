from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);files=list((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_14').glob('*.mqh'))+list((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_14').glob('*.mq5'));assert files
for p in files:
 t=p.read_text(encoding='utf-8');assert 'SAED_V4_14' in t or 'SAEDV414' in t,p
 for banned in ['WebRequest(','OrderSend(','trade.Buy(','trade.Sell(']:assert banned not in t,(p,banned)
print(f'SAED V4-14 MQL5 static validation passed: {len(files)} files')
