from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
paths=[root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i12/python/fp_i12_operator',root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12']
forbidden=('OrderSend','CTrade','PositionOpen','PositionClose','WebRequest','PERIOD_CURRENT')
bad=[]
for base in paths:
 for p in base.rglob('*'):
  if p.is_file():
   if p.name in ('constants.py','authority.py'):continue
   t=p.read_text(encoding='utf-8',errors='ignore')
   for x in forbidden:
    if x in t:bad.append((str(p),x))
print('PASS' if not bad else bad);raise SystemExit(1 if bad else 0)
