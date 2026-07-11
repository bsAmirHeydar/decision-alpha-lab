from pathlib import Path

def repo():return Path(__file__).resolve().parents[4]

def test_required_mql5_and_docs_exist():
    r=repo();assert (r/"mql5/Include/AlphaLab/StrategyFactory/Monitoring/SF19_AllMonitoring.mqh").is_file();assert (r/"docs/strategy_factory_implementation/phase19/00_PHASE_19_MOC.md").is_file();assert (r/"docs/obsidian_deep/00_mocs/STRATEGY_FACTORY_PHASE19_OBSERVABILITY_DRIFT_MOC.md").is_file()

def test_no_live_authority_in_monitoring():
    text="\n".join(p.read_text(errors="ignore") for p in (repo()/"mql5/Include/AlphaLab/StrategyFactory/Monitoring").rglob("*.mqh"))
    for token in ("OrderSend(","OrderCheck(","OrderSendAsync(","CTrade","PositionClose(","WebRequest(","FileOpen("):assert token not in text

def test_phase_status_and_handoff_exist():
    r=repo();assert (r/"lab/11_strategy_factory/implementation_program/phase_status/PHASE_19.json").is_file();assert (r/"lab/11_strategy_factory/implementation_program/phase_status/PHASE_19_HANDOFF_TO_PHASE_20.json").is_file()
