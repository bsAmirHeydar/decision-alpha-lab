from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
files=list((root/'mql5/Include/AlphaLab/StrategyFactory/Anatomy').rglob('*.mqh'))+list((root/'mql5/Experts/StrategyFactory').glob('SF06_*.mq5'))+list((root/'mql5/Experts/StrategyFactoryTests').glob('SF06_*.mq5'))
text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in files)
viol=[]
for token in ('OrderSend(','OrderCheck(','CTrade ','PositionOpen('):
    if token in text:viol.append('live authority: '+token)
ref=(root/'mql5/Include/AlphaLab/StrategyFactory/Anatomy/Reference/SF06_ReferenceSweepPlugin.mqh').read_text(encoding='utf-8')
for token in ('NDS','EXP0017','Daye','ICT','Astro'):
    if token in ref:viol.append('legacy coupling: '+token)
if viol:
    print('\n'.join(viol));raise SystemExit(1)
print('SF06 boundary guard: PASS')
