from dataclasses import dataclass
from strategy_factory_contracts.hashing import stable_id
from .descriptor import PluginDescriptor
from .enums import *
from .requirements import DataRequirement,PluginRequirements
@dataclass(frozen=True,slots=True)
class FixturePulsePlugin: descriptor:PluginDescriptor;requirements:PluginRequirements
class FixturePulseFactory:
    def __init__(self,symbol="EURUSD",timeframe_seconds=60,lookback_bars=32,ticks_per_event=10):
        self._descriptor=PluginDescriptor("sf04.fixture.pulse","SF04 Fixture Pulse Anatomy","1.0.0",PluginKind.ANATOMY,"alpha_lab.strategy_factory","1.0.0",Capability.TICK_INPUT|Capability.CLOSED_BAR_INPUT|Capability.REPLAY_SAFE|Capability.DETERMINISTIC|Capability.FAST_PATH_SAFE|Capability.STATEFUL|Capability.EMITS_CLUSTER_ID|Capability.REQUIRES_SYMBOL_SPEC,UpdateScope.TICK|UpdateScope.TIMER|UpdateScope.REPLAY,128,QueueOverflowPolicy.FAIL_PLUGIN,True,True,True,True,"Synthetic fixture",stable_id("cfg",f"{symbol}|{timeframe_seconds}|{lookback_bars}|{ticks_per_event}"))
        self._requirements=PluginRequirements((DataRequirement("primary_tick",RequirementKind.TICK,RequirementStrength.REQUIRED,symbol,max_staleness_msc=5000),DataRequirement("primary_closed_bars",RequirementKind.CLOSED_BARS,RequirementStrength.REQUIRED,symbol,timeframe_seconds,lookback_bars,timeframe_seconds*3000,0,"fixture_primary"),DataRequirement("primary_symbol_spec",RequirementKind.SYMBOL_SPEC,RequirementStrength.REQUIRED,symbol)))
    @property
    def descriptor(self):return self._descriptor
    @property
    def requirements(self):return self._requirements
    def create(self):return FixturePulsePlugin(self.descriptor,self.requirements)
