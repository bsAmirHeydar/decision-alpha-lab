from __future__ import annotations
from dataclasses import dataclass
from .enums import Compatibility
from .validation import require, validate_safe_identifier

@dataclass(frozen=True, slots=True)
class SchemaIdentity:
    schema_namespace: str
    schema_name: str
    major: int
    minor: int
    patch: int

    def __post_init__(self) -> None:
        validate_safe_identifier(self.schema_namespace, "schema_namespace")
        validate_safe_identifier(self.schema_name, "schema_name")
        require(self.major >= 0 and self.minor >= 0 and self.patch >= 0, "negative schema version")

    @property
    def key(self) -> str:
        return f"{self.schema_namespace}/{self.schema_name}"

    @property
    def version(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def canonical(self) -> str:
        return f"{self.key}@{self.version}"

    def compatibility_with(self, consumer: "SchemaIdentity") -> Compatibility:
        if self.key != consumer.key or self.major != consumer.major:
            return Compatibility.INCOMPATIBLE
        if self.minor <= consumer.minor:
            return Compatibility.COMPATIBLE
        return Compatibility.COMPATIBLE_WITH_MIGRATION
