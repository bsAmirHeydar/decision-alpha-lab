from tools.repository_paths import find_repository_root
from pathlib import Path

def test_contract_kernel_contains_no_trade_authority_or_training_framework():
    root=find_repository_root(__file__)
    owned=[root/"mql5/Include/AlphaLab/StrategyFactory/Contracts",root/"src/engine/packages/strategy_factory_contracts_v3"]
    forbidden=("OrderSend(","OrderCheck(","CTrade","PositionOpen(","sklearn","torch","tensorflow","xgboost","lightgbm")
    for directory in owned:
        for path in directory.rglob("*"):
            if path.suffix.lower() not in {".py",".mqh",".mq5"}:continue
            text=path.read_text(errors="ignore")
            for token in forbidden:assert token not in text,f"forbidden token {token} in {path}"

def test_mql5_uses_repository_approved_integer_serialization():
    root=find_repository_root(__file__)
    for path in (root/"mql5").rglob("UCE03_*"):
        if path.suffix not in {".mqh",".mq5"}:continue
        text=path.read_text(errors="ignore")
        assert "LongToString(" not in text
