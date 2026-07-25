from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
targets=list((ROOT/'src/engine/packages/saed_v4_distributional_survival_tail').glob('*.py'))
banned=['Order'+'Send(','Web'+'Request(','C'+'Trade ','trade.'+'Buy(','trade.'+'Sell(','Meta'+'Trader5','ml'+'flow','wand'+'b','open'+'ai','requests'+'.','socket'+'.']
for p in targets:
 t=p.read_text(encoding='utf-8')
 for x in banned:assert x not in t,(p,x)
print(f'SAED V4-16 boundary guard passed: {len(targets)} Python files')
