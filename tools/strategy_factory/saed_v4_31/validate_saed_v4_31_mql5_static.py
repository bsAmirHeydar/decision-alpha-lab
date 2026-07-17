from __future__ import annotations
import re
from _common import MQL_INCLUDE,MQL_EXPERT
paths=list(MQL_INCLUDE.glob("*.mqh"))+list(MQL_EXPERT.glob("*.mq5")); assert len(paths)==22
for path in paths:
 text=path.read_text(encoding="utf-8")
 for forbidden in [r"OrderSend",r"CTrade",r"TRADE_ACTION_DEAL",r"PositionOpen",r"Buy\s*\(",r"Sell\s*\("]:
  if re.search(forbidden,text): raise AssertionError(f"forbidden execution token in {path}")
 assert "SAED_V4_31" in text and "RESEARCH_ONLY" in text
 if path.suffix==".mqh": assert "#ifndef" in text and "#define" in text and "#endif" in text
print(f"V4-31 MQL5 static validation passed: {len(paths)} files")
