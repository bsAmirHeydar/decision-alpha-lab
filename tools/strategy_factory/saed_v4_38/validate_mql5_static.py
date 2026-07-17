import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];roots=[ROOT/'mql5/Include/StrategyFactory/SAED/V4_38',ROOT/'mql5/Experts/StrategyFactory/SAED/V4_38'];files=[p for r in roots for p in r.rglob('*') if p.suffix.lower() in {'.mqh','.mq5'}]
if len(files)<24:raise SystemExit(f'expected >=24 MQL5 files, got {len(files)}')
for p in files:
 s=p.read_text(encoding='utf-8')
 if 'SAED_V4_38' not in s:raise SystemExit(f'missing phase marker {p}')
 for token in ['OrderSend(','CTrade','trade.Buy','trade.Sell','PositionOpen(','WebRequest(','ShellExecute']:
  if token in s:raise SystemExit(f'forbidden token {token}: {p}')
print(json.dumps({'phase':'SAED_V4_38','mql5_files':len(files),'evidence_kind':'static_only','metaeditor_compile_claimed':False,'passed':True}))
