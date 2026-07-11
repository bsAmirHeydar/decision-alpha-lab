from __future__ import annotations
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[2]
owned=root/"mql5/Include/AlphaLab/StrategyFactory/Execution"
errors=[]
for file in list(owned.rglob("*.mqh"))+list((root/"mql5/Experts/StrategyFactory").glob("SF17_*.mq5"))+list((root/"mql5/Experts/StrategyFactoryTests").glob("SF17_*.mq5")):
    text=file.read_text(errors="ignore")
    if text.count("{") != text.count("}"):
        errors.append(f"brace mismatch: {file.relative_to(root)}")
    for inc in re.findall(r'#include\s+"([^"]+)"',text):
        target=(file.parent/inc).resolve()
        if not target.exists(): errors.append(f"missing include {inc}: {file.relative_to(root)}")
    if "LongToString(" in text: errors.append(f"unsupported LongToString: {file.relative_to(root)}")
if errors:
    print("\n".join(errors));sys.exit(1)
print("SF17 MQL5 static audit PASS")
