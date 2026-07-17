from __future__ import annotations
from _common import MQL_INCLUDE,MQL_EXPERT
files=list(MQL_INCLUDE.glob("*.mqh"))+list(MQL_EXPERT.glob("*.mq5"));assert len(files)>=20
for p in files:
 t=p.read_text(encoding="utf-8"); assert "SAED_V4_34" in t; assert "OrderSend(" not in t and "CTrade" not in t and "trade.Buy" not in t and "trade.Sell" not in t
print(f"V4-34 MQL5 static validation passed: {len(files)} files")
