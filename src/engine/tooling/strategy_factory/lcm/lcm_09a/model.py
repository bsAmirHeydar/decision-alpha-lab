from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class SetupFreezeCounts:
    setup_identities:int
    families:int
    variants:int
    contracts:int
    embedded_candidates:int
    open_unknowns:int
    implementation_authorized:int
