from __future__ import annotations
from _common import MQL_INCLUDE, MQL_EXPERT
paths = sorted(MQL_INCLUDE.glob("*.mqh")) + sorted(MQL_EXPERT.glob("*.mq5"))
assert len(paths) == 24
text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
for token in ["SAED_V4_32", "research_only", "promotion_authority", "execution_authority", "live_trading_authority", "quarantine"]:
    assert token in text
for forbidden in ["OrderSend(", "CTrade", "trade.Buy(", "trade.Sell(", "WebRequest(", "TerminalInfoString(TERMINAL_DATA_PATH)"]:
    assert forbidden not in text
for p in paths:
    t = p.read_text(encoding="utf-8")
    assert "#property strict" in t or p.suffix == ".mqh"
print(f"V4-32 MQL5 static validation passed: {len(paths)} files")
