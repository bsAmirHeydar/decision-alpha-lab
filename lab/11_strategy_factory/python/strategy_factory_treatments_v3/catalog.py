from __future__ import annotations
from dataclasses import dataclass
from .enums import TreatmentKind
from .registry import ExactAtomRegistry
from .entry import ENTRY_ATOMS
from .stop import STOP_ATOMS
from .target import TARGET_ATOMS
from .trailing import TRAILING_ATOMS
from .management import MANAGEMENT_ATOMS
from .sizing import SIZING_ATOMS
@dataclass(slots=True)
class TreatmentCatalog:
 entry:ExactAtomRegistry; stop:ExactAtomRegistry; target:ExactAtomRegistry; trailing:ExactAtomRegistry; management:ExactAtomRegistry; sizing:ExactAtomRegistry
 def registries(self): return (self.entry,self.stop,self.target,self.trailing,self.management,self.sizing)
 def freeze(self):
  for r in self.registries(): r.freeze()
 @property
 def atom_count(self): return sum(len(r.all()) for r in self.registries())
 def resolve_exact_key(self,key:str):
  atom_id,version=key.rsplit('@',1)
  for r in self.registries():
   try:return r.resolve(atom_id,version)
   except Exception: pass
  raise KeyError(key)
def build_default_catalog(freeze:bool=True):
 regs={k:ExactAtomRegistry(k) for k in TreatmentKind}
 groups={TreatmentKind.ENTRY:ENTRY_ATOMS,TreatmentKind.STOP:STOP_ATOMS,TreatmentKind.TARGET:TARGET_ATOMS,TreatmentKind.TRAILING:TRAILING_ATOMS,TreatmentKind.MANAGEMENT:MANAGEMENT_ATOMS,TreatmentKind.SIZING:SIZING_ATOMS}
 for k,classes in groups.items():
  for cls in classes: regs[k].register(cls())
 c=TreatmentCatalog(regs[TreatmentKind.ENTRY],regs[TreatmentKind.STOP],regs[TreatmentKind.TARGET],regs[TreatmentKind.TRAILING],regs[TreatmentKind.MANAGEMENT],regs[TreatmentKind.SIZING])
 if freeze:c.freeze()
 return c
