from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
paths=sorted((ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_27").glob("*.mqh"))+sorted((ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_27").glob("*.mq5"))
assert len(paths)==16,len(paths)
forbidden=("OrderSend(","WebRequest(","CTrade ","trade.Buy(","trade.Sell(","MqlTradeRequest","TerminalInfoString(TERMINAL_DATA_PATH")
for p in paths:
    text=p.read_text(encoding="utf-8")
    assert "SAEDV427" in text or "SAED_V4_27" in text,p
    for token in forbidden: assert token not in text,(p,token)
assert "SAEDV427CanExecute(){return false;}" in (ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_27/SAEDV427Authority.mqh").read_text(encoding="utf-8")
print("V4-27 MQL5 static validation passed: 16 files")
