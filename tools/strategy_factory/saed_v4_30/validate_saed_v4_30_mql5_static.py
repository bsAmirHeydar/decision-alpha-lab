from __future__ import annotations
import re
from _common import MQL_INCLUDE,MQL_EXPERT
files=sorted(MQL_INCLUDE.glob("*.mqh"))+sorted(MQL_EXPERT.glob("*.mq5"))
assert len(files)==22,len(files)
forbidden=[r"\bOrderSend\s*\(",r"\bOrderSendAsync\s*\(",r"\bCTrade\b",r"\.Buy\s*\(",r"\.Sell\s*\(",r"\bTRADE_ACTION_DEAL\b",r"\bTRADE_ACTION_PENDING\b"]
for path in files:
 text=path.read_text(encoding="utf-8")
 assert "SAEDV430" in text or "SAED V4-30" in text,path
 for pattern in forbidden:
  if re.search(pattern,text): raise AssertionError(f"forbidden execution API {pattern} in {path}")
harness=MQL_EXPERT/"SAEDV430ReplicationHarness.mq5"
text=harness.read_text(encoding="utf-8")
assert "#property strict" in text and "void OnTick() { }" in text
print("V4-30 MQL5 static validation passed: 22 files; MetaEditor compile not claimed")
