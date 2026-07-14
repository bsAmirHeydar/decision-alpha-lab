from pathlib import Path
import sys
root=Path(__file__).resolve().parents[2]
phase=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i15'
forbidden=('phase_i16','live_order_submission = true','LIVE_QUOTA_POLICY = "FILLED"')
viol=[]
for p in list((phase/'python').rglob('*.py'))+list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I15').glob('*.mqh')):
 t=p.read_text(errors='ignore')
 for x in forbidden:
  if x in t: viol.append((str(p),x))
print({'status':'PASS' if not viol else 'FAIL','violations':viol})
raise SystemExit(1 if viol else 0)
