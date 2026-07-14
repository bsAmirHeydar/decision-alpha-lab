from pathlib import Path
import sys
root=Path(__file__).resolve().parents[2]
inc=root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I13';entry=root/'mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I13_ReleaseSelfTest.mq5';prod=root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5'
errors=[]
if len(list(inc.glob('*.mqh')))<10:errors.append('insufficient includes')
for p in (entry,prod):
 t=p.read_text(encoding='utf-8');
 if '#property strict' not in t:errors.append(f'{p.name}: strict missing')
 if 'I13/FP_I13_All.mqh' not in t:errors.append(f'{p.name}: I13 include missing')
 if 'PERIOD_CURRENT' in t:errors.append(f'{p.name}: PERIOD_CURRENT forbidden')
print({'status':'PASS' if not errors else 'FAIL','errors':errors})
raise SystemExit(1 if errors else 0)
