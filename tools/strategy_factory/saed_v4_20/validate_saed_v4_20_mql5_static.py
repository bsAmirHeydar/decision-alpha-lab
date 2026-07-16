from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]
files=sorted((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_20').glob('*.mqh'))+sorted((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_20').glob('*.mq5'))
assert len(files)>=18
for f in files:
 t=f.read_text(encoding='utf-8');assert '#property strict' in t;assert 'SAED_V4_20' in t
 assert not re.search(r'OrderSend\s*\(|trade\.(Buy|Sell|PositionOpen)|WebRequest\s*\(',t,re.I),f
print(f'SAED V4-20 MQL5 static validation passed: {len(files)} files; MetaEditor evidence remains external')
