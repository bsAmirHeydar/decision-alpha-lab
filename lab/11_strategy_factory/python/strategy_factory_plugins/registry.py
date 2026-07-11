from dataclasses import dataclass
from .descriptor import PluginSelection
from .enums import PluginKind
@dataclass(frozen=True,slots=True)
class RegisteredFactory: descriptor:object;requirements:object;create:object
class StaticPluginRegistry:
    def __init__(self): self._items={}
    def register(self,factory):
        d=factory.descriptor
        if d.kind is not PluginKind.ANATOMY: raise ValueError("anatomy registry only")
        key=(d.plugin_id,d.version)
        if key in self._items: raise ValueError("duplicate plugin identity")
        self._items[key]=RegisteredFactory(d,factory.requirements,factory.create)
    def resolve(self,s:PluginSelection):
        key=(s.plugin_id,s.exact_version)
        if key not in self._items: raise KeyError(key)
        r=self._items[key]
        if not s.matches(r.descriptor): raise ValueError("selection mismatch")
        return r
    def create(self,s):
        r=self.resolve(s);instance=r.create()
        if getattr(instance,"descriptor",None)!=r.descriptor: raise ValueError("factory-instance descriptor mismatch")
        return instance
    def descriptors(self): return tuple(self._items[k].descriptor for k in sorted(self._items))
    def __len__(self): return len(self._items)
