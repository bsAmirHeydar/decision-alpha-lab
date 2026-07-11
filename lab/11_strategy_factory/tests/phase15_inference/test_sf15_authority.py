from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_phase15_has_prediction_but_no_execution_authority():
    paths=list((ROOT/"mql5/Include/AlphaLab/StrategyFactory/Inference").glob("*.mqh"))+list((ROOT/"mql5/Experts/StrategyFactory").glob("SF15_*.mq5"))
    text="\n".join(p.read_text() for p in paths)
    assert "OnnxRun(" in text
    for token in ("Order"+"Send(","Order"+"Check(","C"+"Trade","Position"+"Open("):
        assert token not in text
