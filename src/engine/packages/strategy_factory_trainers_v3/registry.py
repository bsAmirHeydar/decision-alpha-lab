from dataclasses import dataclass
from .capabilities import CapabilityMatcher
from .errors import CapabilityError
@dataclass(frozen=True,slots=True)
class RegistryEntry: descriptor:object;factory:object
class TrainerRegistry:
 def __init__(self):self._e={};self._frozen=False
 @property
 def frozen(self):return self._frozen
 def freeze(self):self._frozen=True;return self
 def register(self,factory):
  if self._frozen:raise CapabilityError('trainer_registry_frozen','registry is immutable after orchestration starts')
  p=factory();d=p.capability();p.dispose()
  if d.key in self._e:raise CapabilityError('duplicate_trainer_key','duplicate trainer',{'trainer_key':d.key})
  self._e[d.key]=RegistryEntry(d,factory)
 def resolve_exact(self,i,v):
  k=f'{i}@{v}'
  if k not in self._e:raise CapabilityError('trainer_not_found','exact trainer not found',{'trainer_key':k})
  return self._e[k]
 def compatible(self,t,s,b):return tuple((e.descriptor,CapabilityMatcher.evaluate(e.descriptor,t,s,b)) for k,e in sorted(self._e.items()) if CapabilityMatcher.evaluate(e.descriptor,t,s,b).compatible)
 def snapshot(self):return tuple(self._e[k].descriptor for k in sorted(self._e))
