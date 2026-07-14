#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];I=ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4DataFoundation';E=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics';files=sorted(I.glob('*.mqh'))+sorted(E.glob('EXP_SAED_V4_01_*.mq5'));forbidden=['OrderSend','CTrade','WebRequest','SocketCreate','PositionOpen','trade.Buy','trade.Sell'];errors=[]
for p in files:
 t=p.read_text(encoding='utf-8')
 for x in forbidden:
  if x in t:errors.append(f'{p}: forbidden {x}')
cat=(I/'DataFoundationCatalog.mqh').read_text()
for x in ['ORDER','BROKER','NETWORK','CONTEXT_MUTATION','RUNTIME_ACTIVATION','RISK','PORTFOLIO']:
 if f'AL_SAED_V4_DATA_{x}_AUTHORITY false' not in cat:errors.append(f'authority constant invalid: {x}')
print(json.dumps({'status':'pass' if not errors else 'fail','files':len(files),'errors':errors},indent=2));raise SystemExit(0 if not errors else 1)
