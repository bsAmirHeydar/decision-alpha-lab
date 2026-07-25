from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4ExecutionTwin').glob('*.mqh'))+list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_09_*.mq5'))
errors=[]
for p in files:
 t=p.read_text(encoding='utf-8')
 if 'OrderSend(' in t or 'CTrade' in t:errors.append(str(p.relative_to(ROOT)))
 if '#property strict' not in t and p.suffix=='.mq5':errors.append(str(p.relative_to(ROOT))+':strict')
if errors:raise SystemExit('MQL5 static validation failed: '+','.join(errors))
print(f'{len(files)} MQL5 files passed static validation; MetaEditor compile remains external')
