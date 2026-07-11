from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .schema import SchemaIdentity
from .validation import ContractValidationError

NS = "alpha_lab.strategy_factory"

@dataclass(frozen=True, slots=True)
class ContractRegistry:
    schemas: tuple[SchemaIdentity, ...]

    def __post_init__(self) -> None:
        keys = [s.key for s in self.schemas]
        if len(keys) != len(set(keys)):
            raise ContractValidationError("duplicate schema key")

    def get(self, schema_name: str) -> SchemaIdentity:
        for schema in self.schemas:
            if schema.schema_name == schema_name:
                return schema
        raise KeyError(schema_name)

    def as_dict(self) -> dict[str, str]:
        return {schema.schema_name: schema.canonical for schema in self.schemas}

def default_registry() -> ContractRegistry:
    return ContractRegistry(tuple(SchemaIdentity(NS, name, 1, 0, 0) for name in (
        "bar_record", "anatomy_event", "feature_value", "feature_snapshot", "artifact_identity"
    )))
