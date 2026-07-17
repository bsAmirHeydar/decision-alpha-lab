from _common import MQL_INCLUDE,MQL_EXPERT
files=list(MQL_INCLUDE.glob("*.mqh"))+list(MQL_EXPERT.glob("*.mq5"));assert len(files)>=18
for p in files:
 t=p.read_text(encoding="utf-8"); assert "SAED_V4_33" in t and "OrderSend(" not in t and "CTrade" not in t
print(f"V4-33 MQL5 static passed: {len(files)} files")
