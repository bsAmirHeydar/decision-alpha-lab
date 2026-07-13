from __future__ import annotations
from .errors import RuntimeContractError
class RuntimeAdapterRegistry:
    def __init__(self):self._items={}
    def register(self,name,adapter,capabilities=()):
        if name in self._items:raise RuntimeContractError('duplicate_adapter','adapter already registered')
        self._items[name]=(adapter,tuple(sorted(set(capabilities))))
    def resolve(self,name,required_capabilities=()):
        if name not in self._items:raise RuntimeContractError('adapter_not_found','adapter not registered')
        adapter,caps=self._items[name];missing=sorted(set(required_capabilities)-set(caps))
        if missing:raise RuntimeContractError('adapter_capability_missing','adapter lacks capabilities',{'missing':missing})
        return adapter
    def snapshot(self):return tuple((k,self._items[k][1]) for k in sorted(self._items))
