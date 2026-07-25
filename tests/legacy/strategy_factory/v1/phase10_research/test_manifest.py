from strategy_factory_research.models import *
from strategy_factory_research.enums import *
def test_manifest_hash():
 m=RunManifest("run","prog","strat","1",1,"gen","plugins","matrix","sim","cost","params","source","EURUSD",60,1,2,FidelityPresetKind.FAST_SCREEN,ObjectiveMode.CONSERVATIVE,1,0,"git","build","src");m.validate();assert m.derived_hash().startswith("rman_")
