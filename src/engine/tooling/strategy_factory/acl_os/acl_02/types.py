from __future__ import annotations
from dataclasses import dataclass,field
from enum import StrEnum
from typing import Any

class Severity(StrEnum): INFO="INFO"; WARNING="WARNING"; ERROR="ERROR"; BLOCKER="BLOCKER"
class ReadinessState(StrEnum): DRAFT_CONTEXT="DRAFT_CONTEXT"; INTAKE_COMPLETE="INTAKE_COMPLETE"; SEMANTIC_REVIEW_REQUIRED="SEMANTIC_REVIEW_REQUIRED"; SEMANTICALLY_VALIDATED="SEMANTICALLY_VALIDATED"
class IntakeDecision(StrEnum): REJECT="REJECT"; NEEDS_INPUT="NEEDS_INPUT"; NEEDS_REVIEW="NEEDS_REVIEW"; ACCEPT_FOR_SEMANTIC_REVIEW="ACCEPT_FOR_SEMANTIC_REVIEW"; ACCEPT_SEMANTICALLY="ACCEPT_SEMANTICALLY"

@dataclass(frozen=True,slots=True)
class Finding:
    code:str; severity:Severity; path:str; message:str; remediation:str; details:dict[str,Any]=field(default_factory=dict)
    def to_dict(self): return {"code":self.code,"severity":self.severity.value,"path":self.path,"message":self.message,"remediation":self.remediation,"details":self.details}

@dataclass(frozen=True,slots=True)
class SectionScore:
    section:str; required_weight:float; earned_weight:float; blockers:int; warnings:int; missing:list[str]=field(default_factory=list)
    @property
    def score(self)->float: return 1.0 if self.required_weight<=0 else round(self.earned_weight/self.required_weight,6)
    def to_dict(self): return {"section":self.section,"required_weight":self.required_weight,"earned_weight":self.earned_weight,"score":self.score,"blockers":self.blockers,"warnings":self.warnings,"missing":self.missing}

def closed(obj:dict[str,Any],allowed:set[str],name:str)->None:
    extra=set(obj)-allowed
    if extra: raise ValueError(f"{name} unknown fields: {sorted(extra)}")
