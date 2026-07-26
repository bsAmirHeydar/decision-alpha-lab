from tools.repository_paths import find_repository_root
from pathlib import Path

def test_phase17_layout_and_no_live_send():
    root=find_repository_root(__file__)
    required=[root/"mql5/Include/AlphaLab/StrategyFactory/Execution/SF17_PaperExecutionEngine.mqh",
      root/"mql5/Experts/StrategyFactory/SF17_PaperShadowHost.mq5",
      root/"docs/history/systems/strategy_factory_implementation/phase17/00_PHASE_17_MOC.md"]
    assert all(p.exists() for p in required)
    owned=[root/"mql5/Include/AlphaLab/StrategyFactory/Execution",root/"mql5/Experts/StrategyFactory/SF17_PaperShadowHost.mq5"]
    text="\n".join(p.read_text(errors="ignore") for x in owned for p in ([x] if x.is_file() else x.rglob("*")) if p.is_file())
    for forbidden in ("OrderSend(","OrderSendAsync(","CTrade","PositionOpen("):
        assert forbidden not in text
