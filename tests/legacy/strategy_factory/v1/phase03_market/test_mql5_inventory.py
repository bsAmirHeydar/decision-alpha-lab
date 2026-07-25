from tools.repository_paths import find_repository_root
from pathlib import Path

REPO = find_repository_root(__file__)
MARKET = REPO / "mql5/Include/AlphaLab/StrategyFactory/Market"

def test_expected_mql5_market_modules_exist() -> None:
    expected = {
        "SF03_TimeKernel.mqh", "SF03_SessionSchedule.mqh", "SF03_TickCache.mqh",
        "SF03_BarCache.mqh", "SF03_NewBarTracker.mqh",
        "SF03_MultiSymbolSync.mqh", "SF03_TerminalMarketSource.mqh",
        "SF03_SymbolSpecCache.mqh", "SF03_MarketDataService.mqh",
        "SF03_MarketServiceBundle.mqh",
    }
    assert expected <= {path.name for path in MARKET.glob("*.mqh")}

def test_terminal_market_api_isolated_to_terminal_source() -> None:
    api_tokens = ("CopyRates(", "SymbolInfoTick(", "SymbolInfoDouble(", "SymbolInfoInteger(")
    offenders = []
    for path in MARKET.glob("*.mqh"):
        text = path.read_text(encoding="utf-8")
        if path.name == "SF03_TerminalMarketSource.mqh":
            continue
        if any(token in text for token in api_tokens):
            offenders.append(path.name)
    assert offenders == []

def test_phase03_has_no_live_order_authority() -> None:
    tokens = ("OrderSend(", "OrderCheck(", "CTrade", "PositionOpen(")
    roots = [
        REPO / "mql5/Include/AlphaLab/StrategyFactory/Market",
        REPO / "mql5/Experts/StrategyFactory/SF03_MarketServicesDiagnostic.mq5",
        REPO / "mql5/Tests/Experts/StrategyFactory/SF03_MarketServicesSelfTest.mq5",
    ]
    offenders = []
    for root in roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                if any(token in text for token in tokens):
                    offenders.append(str(path.relative_to(REPO)))
    assert offenders == []
