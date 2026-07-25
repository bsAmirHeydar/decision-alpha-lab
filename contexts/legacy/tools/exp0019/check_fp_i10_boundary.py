from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
paths=list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I10').glob('*.mqh'))+list((root/'mql5/Indicators/EXP0019').rglob('*I10*.mq5'))+list((root/'mql5/Indicators/EXP0019/FaerieProtocol').glob('EXP0019_FaerieProtocol_Context.mq5'))
forbidden=['OrderSend(','OrderSendAsync(','CTrade','PositionOpen(','PositionClose(','WebRequest(','ObjectCreate(','ObjectDelete(','ChartSetSymbolPeriod(']
hits=[]
for p in paths:
 t=p.read_text(encoding='utf-8',errors='ignore')
 for token in forbidden:
  if token in t:hits.append([p.relative_to(root).as_posix(),token])
print(json.dumps({'files':len(paths),'hits':hits,'pass':not hits},indent=2)); raise SystemExit(1 if hits else 0)
