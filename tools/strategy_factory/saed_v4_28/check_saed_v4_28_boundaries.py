from pathlib import Path
FORBIDDEN=["OrderSend(","CTrade ","trade.Buy(","trade.Sell(","WebRequest(","production_authority = true","promotion_authority = true"]
ROOT=Path(__file__).resolve().parents[3]; paths=[]
for d in [ROOT/"lab/11_strategy_factory/python/saed_v4_anytime_valid_online_fdr",ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_28",ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_28"]: paths+=list(d.glob("**/*"))
for p in paths:
    if p.is_file():
        t=p.read_text(encoding="utf-8",errors="ignore")
        for x in FORBIDDEN: assert x not in t,(p,x)
print(f"V4-28 authority boundary passed: {sum(p.is_file() for p in paths)} files")
