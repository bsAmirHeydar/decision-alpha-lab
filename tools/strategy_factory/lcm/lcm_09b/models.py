from __future__ import annotations
from dataclasses import dataclass,field
from enum import StrEnum
from typing import Any
class PackageStatus(StrEnum):
    REFERENCE_READY="REFERENCE_READY"
    REFERENCE_BLOCKED="REFERENCE_BLOCKED"
    RETIRED="RETIRED"
class DecisionState(StrEnum):
    ELIGIBLE="ELIGIBLE";TRIGGERED="TRIGGERED";CONFIRMED="CONFIRMED";INVALIDATED="INVALIDATED";CANCELLED="CANCELLED";EXPIRED="EXPIRED";ABSTAINED="ABSTAINED";BLOCKED="BLOCKED"
class ParityStatus(StrEnum):
    PASS="PASS";FAIL="FAIL";BLOCKED="BLOCKED";UNKNOWN="UNKNOWN"
@dataclass(frozen=True,slots=True)
class ContextSnapshot:
    context_identity_id:str;context_version:str;occurrence_id:str;observed_at:str;available_at:str
    features:dict[str,Any]=field(default_factory=dict);states:tuple[str,...]=();known_time_complete:bool=True;source_digest:str=""
@dataclass(frozen=True,slots=True)
class SetupRuntimeState:
    setup_id:str;occurrence_id:str;last_sequence:int=0;state:DecisionState=DecisionState.ABSTAINED;reason_codes:tuple[str,...]=()
