import pytest
from strategy_factory_plugins.enums import *
from strategy_factory_plugins.fixture import FixturePulseFactory
from strategy_factory_plugins.requirements import DataRequirement,PluginRequirements
from strategy_factory_plugins.startup import validate_requirements

def test_requirements_hash_and_duplicates():
 r=FixturePulseFactory().requirements;assert r.requirements_hash.startswith("req_");assert len(r.items)==3
 with pytest.raises(ValueError):PluginRequirements((r.items[0],r.items[0]))

class Probe:
 def __init__(self,fail=False):self.fail=fail
 def ensure_symbol(self,s):
  if self.fail:raise RuntimeError("unavailable")
 def refresh_tick(self,s):self.ensure_symbol(s)
 def refresh_symbol_spec(self,s):self.ensure_symbol(s)
 def refresh_closed_bars(self,s,t,l):self.ensure_symbol(s);return l
 def latest_closed_bar_time_msc(self,s,t):return 99000
 def now_utc_msc(self):return 100000

def test_startup_required_and_optional():
 req=PluginRequirements((DataRequirement("x",RequirementKind.TICK,RequirementStrength.REQUIRED,"BAD"),))
 assert not validate_requirements(req,Probe(True)).ready
 opt=PluginRequirements((DataRequirement("x",RequirementKind.TICK,RequirementStrength.OPTIONAL,"BAD"),))
 assert validate_requirements(opt,Probe(True)).ready
