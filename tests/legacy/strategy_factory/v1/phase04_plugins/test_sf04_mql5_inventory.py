from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
PLUGIN=ROOT/"mql5/Include/AlphaLab/StrategyFactory/Plugins"
def test_files_and_no_authority():
 required={"SF04_PluginDescriptor.mqh","SF04_AnatomyEventQueue.mqh","ISF04_AnatomyPlugin.mqh","SF04_AnatomyPluginBase.mqh","SF04_PluginRegistry.mqh","SF04_PluginStartupValidator.mqh","SF04_AllPlugins.mqh"}
 assert required<={p.name for p in PLUGIN.rglob("*.mqh")}
 for p in PLUGIN.rglob("*.mqh"):
  t=p.read_text();assert not any(x in t for x in ("OrderSend(","OrderCheck(","CTrade","PositionOpen("))
def test_host_is_composition_root():
 t=(ROOT/"mql5/Experts/StrategyFactory/SF04_StrategyHost.mq5").read_text()
 assert "g_registry" in t and "BindAnatomy" in t
 assert not any(x in t for x in ("HookAfterF3","DivergenceStrength","F3Locked","ZoneInvalidation"))
