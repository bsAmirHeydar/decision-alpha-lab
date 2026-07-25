from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_mql5_files_exist():
    base=ROOT/"mql5/Include/AlphaLab/StrategyFactory/Candidate"
    required=["SF08_AllCandidate.mqh","SF08_CandidateEngine.mqh","SF08_PolicyRegistry.mqh","SF08_CandidateMatrixPlan.mqh","SF08_TradeCandidate.mqh"]
    assert all((base/x).exists() for x in required)
def test_no_live_authority_in_phase08():
    paths=list((ROOT/"mql5/Include/AlphaLab/StrategyFactory/Candidate").rglob("*.mqh"))+list((ROOT/"mql5/Experts/StrategyFactory").glob("SF08_*.mq5"))+list((ROOT/"mql5/Tests/Experts/StrategyFactory").glob("SF08_*.mq5"))
    text="\n".join(p.read_text(encoding="utf-8") for p in paths)
    forbidden=["OrderSend(","OrderCheck(","CTrade","PositionOpen("]
    assert not any(x in text for x in forbidden)
def test_no_long_to_string():
    text="\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"mql5").rglob("SF08_*.mq*"))
    assert "LongToString(" not in text
