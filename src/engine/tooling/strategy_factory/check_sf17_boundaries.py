from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
root=find_repository_root(__file__)
owned=[root/"mql5/Include/AlphaLab/StrategyFactory/Execution",root/"mql5/Experts/StrategyFactory/SF17_PaperShadowHost.mq5",root/"mql5/Experts/StrategyFactory/SF17_ExecutionDiagnostic.mq5"]
text="\n".join(p.read_text(errors="ignore") for x in owned for p in ([x] if x.is_file() else x.rglob("*")) if p.is_file())
forbidden=("OrderSend(","OrderSendAsync(","CTrade","PositionOpen(","WebRequest(")
hits=[x for x in forbidden if x in text]
if hits:
    print("SF17 boundary failure:",hits);sys.exit(1)
print("SF17 boundaries PASS: paper/shadow only, no broker send authority")
