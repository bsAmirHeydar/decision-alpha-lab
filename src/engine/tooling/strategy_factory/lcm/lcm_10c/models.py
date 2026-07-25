from __future__ import annotations
from dataclasses import dataclass,field
from enum import StrEnum
from typing import Any
class LifecycleState(StrEnum):
    CREATED="CREATED";VALIDATING="VALIDATING";REJECTED="REJECTED";DRY_RUN_ACCEPTED="DRY_RUN_ACCEPTED";EXECUTION_BLOCKED="EXECUTION_BLOCKED";CANCELLED="CANCELLED";EXPIRED="EXPIRED";RECONCILIATION_BLOCKED="RECONCILIATION_BLOCKED"
class SafetyCode(StrEnum):
    DUPLICATE_DECISION="DUPLICATE_DECISION";STALE_QUOTE="STALE_QUOTE";EXCESSIVE_SPREAD="EXCESSIVE_SPREAD";INVALID_TICK_ALIGNMENT="INVALID_TICK_ALIGNMENT";INVALID_VOLUME="INVALID_VOLUME";INVALID_STOP_DISTANCE="INVALID_STOP_DISTANCE";CLOSED_SESSION="CLOSED_SESSION";MISSING_QUOTE="MISSING_QUOTE";RECONCILIATION_MISMATCH="RECONCILIATION_MISMATCH";KILL_SWITCH_ACTIVE="KILL_SWITCH_ACTIVE";UNSUPPORTED_ENTRY="UNSUPPORTED_ENTRY";MISSING_REQUIRED_FIELD="MISSING_REQUIRED_FIELD"
@dataclass(frozen=True,slots=True)
class SafetyFinding:
    code:str;field:str;message:str;blocking:bool=True;details:dict[str,Any]=field(default_factory=dict)
    def to_dict(self):return {"code":self.code,"field":self.field,"message":self.message,"blocking":self.blocking,"details":self.details}
