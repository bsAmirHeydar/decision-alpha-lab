from tools.repository_paths import find_repository_root
from pathlib import Path
import json,re
ROOT=find_repository_root(__file__);bases=[ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_21',ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_21']
files=sorted(p for b in bases for p in b.rglob('*') if p.suffix.lower() in {'.mqh','.mq5'});assert len(files)>=18
forbidden=['OrderSend','CTrade','WebRequest','Socket','FileOpen','TerminalInfoString(TERMINAL_DATA_PATH','ExpertRemove']
for p in files:
 t=p.read_text(encoding='utf-8');assert not any(x in t for x in forbidden),p
 if p.suffix.lower()=='.mqh':assert '#ifndef' in t and '#define' in t and '#endif' in t
print(json.dumps({'passed':True,'mql5_static_files':len(files),'metaeditor_compile':'pending_local_windows'},sort_keys=True))
