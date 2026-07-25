from __future__ import annotations
from dataclasses import dataclass,field
from enum import StrEnum
from typing import Any
class Side(StrEnum): BUY="BUY"; SELL="SELL"; UNKNOWN="UNKNOWN"
class EntryKind(StrEnum): MARKET="MARKET"; LIMIT="LIMIT"; STOP="STOP"; STOP_LIMIT="STOP_LIMIT"; UNSPECIFIED="UNSPECIFIED"
class AdapterMode(StrEnum): REFERENCE="REFERENCE"; DRY_RUN="DRY_RUN"; PAPER="PAPER"; LIVE="LIVE"
class IntentStatus(StrEnum): VALID_REFERENCE="VALID_REFERENCE"; BLOCKED="BLOCKED"; REJECTED="REJECTED"
@dataclass(frozen=True,slots=True)
class Finding:
    code:str;field:str;message:str;blocking:bool=True;details:dict[str,Any]=field(default_factory=dict)
    def to_dict(self):return {"code":self.code,"field":self.field,"message":self.message,"blocking":self.blocking,"details":self.details}
