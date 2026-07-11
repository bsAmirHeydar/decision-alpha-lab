from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_mql5_files():
 paths=[ROOT/"mql5/Include/AlphaLab/StrategyFactory/Research/SF10_AllResearch.mqh",ROOT/"mql5/Experts/StrategyFactoryTests/SF10_ResearchHarnessSelfTest.mq5",ROOT/"mql5/Experts/StrategyFactory/SF10_StrategyTesterResearchHost.mq5"]
 assert all(p.exists() for p in paths)
def test_no_authority_or_unsupported_serialization():
 text="\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"mql5").rglob("SF10_*.*"));assert "OrderSend(" not in text and "CTrade" not in text and "LongToString" not in text
