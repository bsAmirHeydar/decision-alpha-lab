from pathlib import Path
import json,sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
paths=list((root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i09').rglob('*'))+list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I09').glob('*'))
forbidden=['OrderSend','CTrade','PositionOpen','WebRequest','ObjectCreate','trade.Buy','trade.Sell']
hits=[]
for p in paths:
 if p.is_file() and p.suffix.lower() in {'.py','.mqh','.mq5'}:
  t=p.read_text(encoding='utf-8',errors='ignore')
  for f in forbidden:
   if f in t: hits.append([str(p),f])
print(json.dumps({'forbidden_hits':hits,'pass':not hits},indent=2)); raise SystemExit(1 if hits else 0)
