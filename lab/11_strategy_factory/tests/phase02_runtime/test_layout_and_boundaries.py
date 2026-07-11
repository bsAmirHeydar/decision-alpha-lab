from pathlib import Path
import json, re
from strategy_factory_runtime.layout import missing_paths
from strategy_factory_runtime.dependency_guard import scan_mql5_boundaries

ROOT = Path(__file__).resolve().parents[4]
RULES = ROOT / "lab/11_strategy_factory/phase02_runtime/config/dependency_rules.json"

def test_required_layout_exists():
    assert missing_paths(ROOT) == []

def test_dependency_guard_clean():
    assert scan_mql5_boundaries(ROOT, RULES) == []

def test_host_is_thin_and_contains_no_anatomy_terms():
    host = (ROOT / "mql5/Experts/StrategyFactory/SF02_StrategyHost.mq5").read_text(encoding="utf-8")
    forbidden = ("HookAfter", "F3", "Divergence", "ZoneAF", "OrderSend(", "CTrade")
    assert not any(x in host for x in forbidden)

def test_runtime_has_no_live_order_authority():
    paths = list((ROOT / "mql5/Include/AlphaLab/StrategyFactory").rglob("*.mqh"))
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in paths)
    for token in ("OrderSend(", "OrderCheck(", "CTrade", "PositionOpen("):
        assert token not in text

def test_mql5_first_port_inventory():
    ports = ROOT / "mql5/Include/AlphaLab/StrategyFactory/Ports"
    expected = {"ISF02_ClockPort.mqh", "ISF02_AnatomyProvider.mqh", "ISF02_FeatureProvider.mqh",
                "ISF02_ResultSink.mqh", "ISF02_MarketDataPort.mqh", "ISF02_SymbolSpecPort.mqh",
                "ISF02_ExecutionBoundary.mqh"}
    assert expected.issubset({p.name for p in ports.iterdir()})
