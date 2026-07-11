from pathlib import Path

def test_phase13_layout_and_no_live_authority():
    root=Path(__file__).resolve().parents[4];headers=list((root/"mql5/Include/AlphaLab/StrategyFactory/Training").glob("*.mqh"))
    assert len(headers)>=10
    text="\n".join(p.read_text(encoding="utf-8") for p in headers)
    for token in ("Order"+"Send(","Order"+"Check(","C"+"Trade","Position"+"Open(","Long"+"ToString("):
        assert token not in text
