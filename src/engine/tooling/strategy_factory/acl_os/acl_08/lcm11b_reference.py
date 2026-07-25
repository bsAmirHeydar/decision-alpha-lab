from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class LCM11BReferencePort:
    migration_id:str
    visualizer_registry_digest:str
    cutover_manifest_digest:str
    handoff_digest:str
    runtime_authority:bool=False
    order_authority:bool=False
    capital_authority:bool=False
    def assert_authority_negative(self)->None:
        if self.runtime_authority or self.order_authority or self.capital_authority:raise RuntimeError("LCM-11B reference port cannot create authority")
