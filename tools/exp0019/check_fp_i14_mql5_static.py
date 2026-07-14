from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
paths=list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I14').glob('*.mqh'))+[root/'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Diagnostic.mq5',root/'mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I14_DiagnosticSelfTest.mq5']
forbidden=['OrderSend','CTrade','PositionOpen','PositionClose','WebRequest','trade.Buy','trade.Sell']
hits=[]
for p in paths:
 t=p.read_text(encoding='utf-8',errors='ignore')
 for x in forbidden:
  if x in t:hits.append([str(p),x])
print(json.dumps({'files':len(paths),'forbidden_hits':hits,'status':'PASS' if not hits else 'FAIL'},indent=2));raise SystemExit(1 if hits else 0)
