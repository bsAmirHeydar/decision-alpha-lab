from __future__ import annotations
from dataclasses import dataclass
from typing import Generic,TypeVar,Iterable
from .contracts import TreatmentAtomDescriptor
from .enums import TreatmentKind
from .errors import RegistryError
from .utils import stable_id
T=TypeVar('T')
class ExactAtomRegistry(Generic[T]):
    def __init__(self,kind:TreatmentKind): self.kind=kind; self._items={}; self._frozen=False
    def register(self,atom:T):
        if self._frozen: raise RegistryError('registry_frozen','registry is frozen')
        d:TreatmentAtomDescriptor=atom.descriptor
        if d.kind is not self.kind: raise RegistryError('kind_mismatch','atom kind does not match registry')
        if d.exact_key in self._items: raise RegistryError('duplicate_exact_key','duplicate exact atom key',{'key':d.exact_key})
        self._items[d.exact_key]=atom
    def freeze(self): self._frozen=True
    def resolve(self,atom_id:str,version:str)->T:
        k=f'{atom_id}@{version}'
        if k not in self._items: raise RegistryError('exact_version_missing','exact atom version not found',{'key':k})
        return self._items[k]
    def all(self)->tuple[T,...]: return tuple(self._items[k] for k in sorted(self._items))
    @property
    def snapshot_id(self): return stable_id('ucers',{'kind':self.kind.value,'definitions':[x.descriptor.definition_id for x in self.all()]})
