#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
paths=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4Constitution').glob('*.mqh'))
paths+=list((ROOT/'mql5/Experts/StrategyFactory').glob('SAED_V4_00_*.mq5'))
paths+=list((ROOT/'mql5/Experts/StrategyFactoryTests').glob('SAED_V4_00_*.mq5'))
banned=[r'\bOrderSend\s*\(',r'\bCTrade\b',r'\btrade\.(Buy|Sell|PositionOpen)',r'\bWebRequest\s*\(',r'\bSocket']
errors=[]
for p in paths:
 text=p.read_text(encoding='utf-8')
 for pat in banned:
  if re.search(pat,text,re.I): errors.append(f'{p.relative_to(ROOT)} contains banned token {pat}')
 if p.suffix=='.mqh' and '#ifndef' not in text: errors.append(f'{p.relative_to(ROOT)} missing include guard')
print(json.dumps({'status':'pass' if not errors else 'fail','files':len(paths),'errors':errors,'metaeditor_compile':'pending_local_windows'},indent=2))
raise SystemExit(0 if not errors else 1)
