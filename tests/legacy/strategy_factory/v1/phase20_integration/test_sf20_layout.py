from tools.repository_paths import find_repository_root
from pathlib import Path

def repo(): return find_repository_root(__file__)

def test_required_layout():
    r=repo()
    assert (r/"mql5/Include/AlphaLab/StrategyFactory/Integration/EXP0017/SF20_EXP0017Plugin.mqh").is_file()
    assert (r/"docs/history/systems/strategy_factory_implementation/phase20/00_PHASE_20_MOC.md").is_file()
    assert (r/"docs/history/obsidian/deep/00_mocs/STRATEGY_FACTORY_PHASE20_EXP0017_INTEGRATION_MOC.md").is_file()

def test_no_broker_authority_in_phase20_integration():
    root=repo()/"mql5/Include/AlphaLab/StrategyFactory/Integration"
    text="\n".join(p.read_text(errors="ignore") for p in root.rglob("*.mqh"))
    for token in ("OrderSend(","OrderCheck(","OrderSendAsync(","CTrade","PositionOpen(","PositionClose(","WebRequest("):
        assert token not in text

def test_phase_status_and_handoff():
    r=repo(); assert (r/"releases/history/strategy_factory/program/implementation/phase_status/PHASE_20.json").is_file(); assert (r/"releases/history/strategy_factory/program/implementation/phase_status/PHASE_20_HANDOFF_TO_PHASE_21.json").is_file()
