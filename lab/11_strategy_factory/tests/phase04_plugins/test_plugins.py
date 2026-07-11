import pytest
from strategy_factory_plugins.descriptor import PluginDescriptor,PluginSelection
from strategy_factory_plugins.enums import *
from strategy_factory_plugins.fixture import FixturePulseFactory
from strategy_factory_plugins.registry import StaticPluginRegistry
from strategy_factory_plugins.queue import AnatomyEventQueue,QueueResult

def test_descriptor_and_selection():
 d=FixturePulseFactory().descriptor
 assert d.descriptor_hash.startswith("plg_")
 assert PluginSelection(d.plugin_id,d.version,Capability.DETERMINISTIC,d.descriptor_hash).matches(d)

def test_fast_path_requires_determinism():
 with pytest.raises(ValueError):PluginDescriptor("bad.plugin","Bad","1.0.0",PluginKind.ANATOMY,"provider","1.0.0",Capability.FAST_PATH_SAFE,UpdateScope.TICK,8,QueueOverflowPolicy.REJECT_NEW,False,False,True,False,"","cfg")

def test_registry_exact_and_duplicate():
 r=StaticPluginRegistry();f=FixturePulseFactory();r.register(f)
 with pytest.raises(ValueError):r.register(f)
 p=r.create(PluginSelection("sf04.fixture.pulse","1.0.0",Capability.TICK_INPUT))
 assert p.descriptor==f.descriptor

def test_queue_policies_and_duplicates():
 q=AnatomyEventQueue(1,QueueOverflowPolicy.FAIL_PLUGIN)
 assert q.push("a",1)==QueueResult.INSERTED
 assert q.push("a",2)==QueueResult.DUPLICATE
 assert q.push("b",2)==QueueResult.FAILED
 assert q.push("c",3)==QueueResult.FAILED
