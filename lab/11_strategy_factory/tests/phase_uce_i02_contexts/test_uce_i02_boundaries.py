from __future__ import annotations
from pathlib import Path

def root(): return Path(__file__).resolve().parents[4]

def test_phase_has_no_order_authority():
    owned=[root()/"mql5/Include/AlphaLab/StrategyFactory/ContextPackage",root()/"mql5/Experts/StrategyFactory/UCE_I02_ContextPackageDiagnostic.mq5",root()/"mql5/Experts/StrategyFactoryTests/UCE_I02_ContextPackageSelfTest.mq5"]
    forbidden=("OrderSend(","OrderCheck(","CTrade","PositionOpen(","Buy(","Sell(")
    for path in owned:
        files=[path] if path.is_file() else list(path.rglob("*.mq*"))
        for f in files:
            text=f.read_text(errors="ignore")
            for token in forbidden: assert token not in text,(f,token)

def test_phase_uses_no_long_to_string():
    for f in (root()/"mql5/Include/AlphaLab/StrategyFactory/ContextPackage").rglob("*.mqh"):
        assert "LongToString(" not in f.read_text(errors="ignore")
