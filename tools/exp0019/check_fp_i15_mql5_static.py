from pathlib import Path
root=Path(__file__).resolve().parents[2]
paths=list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I15').glob('*.mqh'))+list((root/'mql5/Experts/EXP0019/FaerieProtocol').glob('*Paper*.mq5'))
forbidden=('OrderSend(','CTrade ','PositionOpen(','PositionClose(','.Buy(','.Sell(','WebRequest(')
viol=[]
for p in paths:
 t=p.read_text(errors='ignore')
 for token in forbidden:
  if token in t: viol.append((str(p),token))
required=('FP_RiskAdapter.mqh','FP_I15_PaperQuota.mqh','FP_I15_PaperSimulator.mqh')
missing=[x for x in required if not (root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I15'/x).exists()]
print({'status':'PASS' if not viol and not missing else 'FAIL','files':len(paths),'violations':viol,'missing':missing})
raise SystemExit(1 if viol or missing else 0)
