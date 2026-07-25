from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__); inc=ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_29"; exp=ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_29"
files=sorted(inc.glob("*.mqh"))+sorted(exp.glob("*.mq5")); assert len(files)>=20
for p in files:
    t=p.read_text(encoding="utf-8"); low=t.lower(); assert ("saedv429" in low or "saed_v4_29" in low) and "webrequest" not in low and "socket" not in low and "ordersend" not in low and "trade.mqh" not in low
assert "return false" in (inc/"SAEDV429Authority.mqh").read_text(encoding="utf-8").lower()
print(f"V4-29 MQL5 static validation passed: {len(files)} files")
