from pathlib import Path
FORBIDDEN=("OrderSend(","WebRequest(","SocketCreate(","trade.Buy(","trade.Sell(","PositionOpen(")
def scan(root:Path):
    findings=[]
    for p in sorted(root.rglob("*")):
        if p.name=="static_validation.py": continue
        if p.suffix.lower() not in (".py",".mqh",".mq5"):continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        for token in FORBIDDEN:
            if token in text:findings.append({"path":p.as_posix(),"token":token})
    return findings
