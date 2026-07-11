from __future__ import annotations
from dataclasses import dataclass
from .enums import Compatibility
from .schema import SchemaIdentity

@dataclass(frozen=True, slots=True)
class CompatibilityDecision:
    status: Compatibility
    reason: str


def check_compatibility(producer: SchemaIdentity, consumer: SchemaIdentity) -> CompatibilityDecision:
    status = producer.compatibility_with(consumer)
    if status == Compatibility.INCOMPATIBLE:
        return CompatibilityDecision(status, "schema key or major version mismatch")
    if status == Compatibility.COMPATIBLE_WITH_MIGRATION:
        return CompatibilityDecision(status, "producer minor version is newer than consumer")
    return CompatibilityDecision(status, "same schema key and compatible major/minor range")
