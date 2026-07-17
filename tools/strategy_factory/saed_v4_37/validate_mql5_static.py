import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; roots=[ROOT/'mql5/Include/StrategyFactory/SAED/V4_37',ROOT/'mql5/Experts/StrategyFactory/SAED/V4_37']; files=[p for r in roots for p in r.rglob('*') if p.suffix.lower() in {'.mqh','.mq5'}]
if len(files)<20:raise SystemExit(f'expected >=20 MQL5 files, got {len(files)}')
for p in files:
 s=p.read_text(encoding='utf-8')
 if 'SAED_V4_37' not in s:raise SystemExit(f'missing phase marker: {p}')
 for forbidden in ['OrderSend(','CTrade','trade.Buy','trade.Sell','WebRequest(','ShellExecute']:
  if forbidden in s:raise SystemExit(f'forbidden authority token {forbidden}: {p}')
print(json.dumps({'phase':'SAED_V4_37','mql5_files':len(files),'passed':True}))
