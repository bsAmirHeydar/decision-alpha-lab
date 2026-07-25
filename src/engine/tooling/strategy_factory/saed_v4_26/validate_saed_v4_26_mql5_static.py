from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__); files=sorted((ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_26").glob("*.mqh"))+sorted((ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_26").glob("*.mq5")); assert len(files)==25,len(files)
forbidden=["OrderSend(","OrderSendAsync(","CTrade",".Buy(",".Sell(","WebRequest(","SocketCreate("]
for p in files:
 t=p.read_text(); assert "SAED" in t and "V4_26" in p.as_posix(); assert not any(x in t for x in forbidden)
 if p.suffix==".mqh": assert "#ifndef" in t and "#define" in t and "#endif" in t
 else: assert "#property strict" in t and "void OnTick" in t
print(f"V4-26 MQL5 static validation passed: {len(files)} files; MetaEditor compile pending_local_windows")
