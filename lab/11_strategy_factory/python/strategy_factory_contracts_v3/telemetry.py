"""Bounded counters for contract-kernel observability."""
from dataclasses import dataclass

@dataclass(slots=True)
class ContractTelemetry:
    canonicalizations:int=0
    identities_built:int=0
    schema_resolutions:int=0
    migrations_applied:int=0
    compatibility_accepts:int=0
    compatibility_rejections:int=0
    causal_rejections:int=0
    legacy_bridges:int=0

    def snapshot(self)->dict[str,int]:
        return {name:getattr(self,name) for name in self.__dataclass_fields__}
