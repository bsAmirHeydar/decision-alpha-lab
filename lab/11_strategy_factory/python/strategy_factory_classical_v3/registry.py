from dataclasses import asdict
from .catalog import CATALOG
from .contracts import AlgorithmRegistrySnapshot
from .dependency import DependencyProbe
from .native_baselines import NATIVE_BASELINES
from .sklearn_plugins import make_plugin_class
from strategy_factory_trainers_v3.canonical import canonical_sha256,stable_id
class ClassicalAlgorithmRegistry:
 def __init__(self,probe=None):self.probe=probe or DependencyProbe();self._descriptors={x.key:x for x in CATALOG};self._frozen=False
 def freeze(self):self._frozen=True;return self
 def descriptor(self,key):return self._descriptors[key]
 def snapshot(self):
  ds=tuple(self._descriptors[k] for k in sorted(self._descriptors));av=tuple(self.probe.evaluate(x) for x in ds);h=canonical_sha256({'d':[asdict(x) for x in ds],'a':[asdict(x) for x in av]});return AlgorithmRegistrySnapshot(stable_id('ucealgreg',h),ds,av,self._frozen,h)
 def available(self):return tuple(x for x in self.snapshot().availability if x.available)
def register_classical_trainers(trainer_registry,include_unavailable=False,probe=None):
 probe=probe or DependencyProbe();registered=[]
 for cls in NATIVE_BASELINES:trainer_registry.register(cls);registered.append(cls.capability().key)
 for d in CATALOG:
  if d.family.value=='baseline':continue
  a=probe.evaluate(d)
  if a.available or include_unavailable:
   cls=make_plugin_class(d.algorithm_id);trainer_registry.register(cls);registered.append(cls.capability().key)
 return tuple(registered)
