from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);inc=ROOT/'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_19';exp=ROOT/'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_19'
files=sorted(inc.glob('*.mqh'));experts=sorted(exp.glob('*.mq5'));assert len(files)>=17 and len(experts)==1
text='\n'.join(f.read_text(encoding='utf-8') for f in files+experts)
for token in ['OrderSend(','CTrade','PositionOpen(','WebRequest(','FileOpen(','SocketCreate(','TerminalInfoString(TERMINAL_DATA_PATH)']:assert token not in text,token
for token in ['SAEDV419CanSelectLiveTreatment(){ return false; }','SAEDV419CanPromote(){ return false; }','SAEDV419CanSendOrder(){ return false; }','SAEDV419RealMechanismClaim(){ return false; }']:assert token in text,token
print(f'SAED V4-19 MQL5 static validation passed: {len(files)+len(experts)} files; MetaEditor compile remains external')
