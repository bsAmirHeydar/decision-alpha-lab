from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
files=list((root/"mql5/Include/AlphaLab/StrategyFactory/Integration").rglob("*.mqh"))+list((root/"mql5/Experts/StrategyFactory").glob("SF20_*.mq5"))+list((root/"mql5/Tests/Experts/StrategyFactory").glob("SF20_*.mq5"))
errors=[]
for p in files:
    s=p.read_text(errors="ignore")
    if "LongToString(" in s: errors.append(f"{p}: LongToString")
    if s.count("{")!=s.count("}"): errors.append(f"{p}: brace mismatch")
    if p.suffix==".mqh" and not re.search(r"#ifndef\s+\S+",s): errors.append(f"{p}: missing include guard")
if errors: raise SystemExit("\n".join(errors))
print(f"SF20 MQL5 static PASS files={len(files)}")
