from tools.repository_paths import find_repository_root
from pathlib import Path
import json,re
ROOT=find_repository_root(__file__);files=sorted((ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_22').glob('*.mqh'))+sorted((ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_22').glob('*.mq5'))
assert len(files)>=19
for p in files:
    t=p.read_text(encoding='utf-8');assert 'SAED_V4_22' in t or 'SAEDV422' in t
    assert not re.search(r'OrderSend\s*\(|CTrade|trade\.Buy|trade\.Sell',t,re.I)
print(json.dumps({'passed':True,'mql5_static_files':len(files),'metaeditor_compile':'pending_local_windows'},sort_keys=True))
