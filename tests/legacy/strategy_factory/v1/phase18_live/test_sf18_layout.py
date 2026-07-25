from tools.repository_paths import find_repository_root
from pathlib import Path

def test_live_authority_is_isolated_to_single_adapter():
    root=find_repository_root(__file__)
    live=root/"mql5/Include/AlphaLab/StrategyFactory/Live"
    files=[p for p in live.rglob("*") if p.is_file()]
    send_files=[]; check_files=[]
    for p in files:
        text=p.read_text(errors="ignore")
        if "OrderSend(" in text: send_files.append(p.name)
        if "OrderCheck(" in text: check_files.append(p.name)
        assert "OrderSendAsync(" not in text
        assert "CTrade" not in text
    assert send_files==["SF18_Mql5BrokerAdapter.mqh"]
    assert check_files==["SF18_Mql5BrokerAdapter.mqh"]

def test_micro_live_host_defaults_locked():
    root=find_repository_root(__file__)
    text=(root/"mql5/Experts/StrategyFactory/SF18_MicroLiveHost.mq5").read_text()
    assert "InpEnableMicroLive=false" in text
    assert "InpStartWithKillSwitchEngaged=true" in text
    assert "OnTick" not in text or "Submit" not in text
