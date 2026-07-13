from dataclasses import asdict
from .catalog import CATALOG
from .contracts import AdvancedTaskRegistrySnapshot
from .canonical import canonical_sha256,stable_id
from .errors import AdvancedTaskError
class AdvancedTaskRegistry:
 def __init__(self):self._d={x.key:x for x in CATALOG};self._frozen=False
 def register(self,descriptor):
  if self._frozen:raise AdvancedTaskError('registry_frozen','advanced task registry is frozen')
  if descriptor.key in self._d:raise AdvancedTaskError('duplicate_algorithm','duplicate algorithm key',{'key':descriptor.key})
  self._d[descriptor.key]=descriptor
 def resolve_exact(self,key):
  if key not in self._d:raise AdvancedTaskError('algorithm_not_found','exact advanced algorithm not found',{'key':key})
  return self._d[key]
 def freeze(self):self._frozen=True;return self
 def snapshot(self):
  ds=tuple(self._d[k] for k in sorted(self._d));h=canonical_sha256([asdict(x) for x in ds]);return AdvancedTaskRegistrySnapshot(stable_id('uceadvreg',h),ds,self._frozen,h)
