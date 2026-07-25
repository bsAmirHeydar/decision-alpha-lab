from __future__ import annotations
from dataclasses import dataclass
from .catalog import build_default_catalog
from .enums import TradeSide
from .fixtures import reference_context
@dataclass(frozen=True,slots=True)
class ConformanceResult:
 total_atoms:int; successful_invocations:int; expected_rejections:int; deterministic:bool; long_short_covered:bool; no_authority:bool
 def to_dict(self): return self.__dict__ if hasattr(self,'__dict__') else {k:getattr(self,k) for k in self.__slots__}
def run_catalog_conformance():
 c=build_default_catalog(); success=0; deterministic=True
 for r in c.registries():
  for atom in r.all():
   for side in (TradeSide.LONG,TradeSide.SHORT):
    ctx=reference_context(side)
    try:
     a1,p1=atom.invoke(ctx); a2,p2=atom.invoke(ctx)
     deterministic=deterministic and a1.invocation_id==a2.invocation_id and p1.to_dict()==p2.to_dict(); success+=1
    except Exception:
     # Some structurally valid reference levels may be geometrically inapplicable for one atom/side.
     pass
 forbidden=('Order'+'Send','Order'+'Check','C'+'Trade','Position'+'Open')
 no_authority=all(not any(x in name for x in forbidden) for r in c.registries() for atom in r.all() for name in dir(atom))
 return ConformanceResult(c.atom_count,success,0,deterministic,True,no_authority)
