from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; paths=sorted((ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_28").glob("*.mqh"))+sorted((ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_28").glob("*.mq5"))
assert len(paths)==20,len(paths)
for p in paths:
    t=p.read_text(encoding="utf-8"); assert ("SAEDV428" in t or "SAED_V4_28" in t),p
    for forbidden in ["OrderSend(","CTrade ","trade.Buy(","trade.Sell(","WebRequest("]: assert forbidden not in t,(p,forbidden)
print(f"V4-28 MQL5 static validation passed: {len(paths)} files; MetaEditor pending local Windows evidence")
