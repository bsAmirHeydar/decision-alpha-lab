from tools.repository_paths import find_repository_root
from pathlib import Path

def test_phase13_layout_and_no_live_authority():
    root=find_repository_root(__file__);headers=list((root/"mql5/Include/AlphaLab/StrategyFactory/Training").glob("*.mqh"))
    assert len(headers)>=10
    text="\n".join(p.read_text(encoding="utf-8") for p in headers)
    for token in ("Order"+"Send(","Order"+"Check(","C"+"Trade","Position"+"Open(","Long"+"ToString("):
        assert token not in text
