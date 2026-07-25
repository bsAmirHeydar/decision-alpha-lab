from __future__ import annotations
import ast,re
from pathlib import Path
FORBIDDEN=(r"\bOrderSend\b",r"\bCTrade\b",r"\bObjectCreate\b",r"\bChartSet",r"\brequests\.",r"\bsocket\.",r"\bsubprocess\.",r"\bMetaTrader5\b")
def scan_module(root:Path)->dict:
    findings=[];files=0
    for p in sorted(root.glob("*.py")):
        if p.name=="static_validation.py": continue
        files+=1;text=p.read_text(encoding="utf-8");ast.parse(text)
        for pattern in FORBIDDEN:
            if re.search(pattern,text):findings.append({"path":p.as_posix(),"pattern":pattern})
    return {"passed":not findings,"python_file_count":files,"findings":findings}
