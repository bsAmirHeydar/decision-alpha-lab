from __future__ import annotations
from pathlib import Path
FORBIDDEN=("OrderSend(","trade.Buy(","trade.Sell(","PositionOpen(","PositionModify(","PositionClose(")

def scan(root: Path):
    findings=[]
    for path in sorted(root.rglob('*')):
        if path.suffix.lower() not in {'.py','.mqh','.md','.json'} or not path.is_file():continue
        text=path.read_text(encoding='utf-8',errors='ignore')
        for token in FORBIDDEN:
            if token in text:findings.append({'path':path.as_posix(),'token':token})
    return findings
