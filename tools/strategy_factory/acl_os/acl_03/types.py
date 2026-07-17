from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class Severity(StrEnum):
    INFO="INFO"; WARNING="WARNING"; ERROR="ERROR"; BLOCKER="BLOCKER"
class CompilationState(StrEnum):
    NOT_STARTED="NOT_STARTED"; SOURCE_FROZEN="SOURCE_FROZEN"; IR_COMPILED="IR_COMPILED"; REPLAY_VALIDATED="REPLAY_VALIDATED"; CONTEXT_COMPILED="CONTEXT_COMPILED"; ONBOARDING_BLOCKED="ONBOARDING_BLOCKED"
class CompileDecision(StrEnum):
    REJECT="REJECT"; NEEDS_INPUT="NEEDS_INPUT"; COMPILE_REFERENCE="COMPILE_REFERENCE"; COMPILED_WITH_OBLIGATIONS="COMPILED_WITH_OBLIGATIONS"
class ArtifactKind(StrEnum):
    SOURCE_SNAPSHOT="SOURCE_SNAPSHOT"; COMPILER_PLAN="COMPILER_PLAN"; DETECTOR_IR="DETECTOR_IR"; OCCURRENCE_IR="OCCURRENCE_IR"; KNOWN_TIME_IR="KNOWN_TIME_IR"; FEATURE_BINDING_IR="FEATURE_BINDING_IR"; ADAPTER_CONTRACT="ADAPTER_CONTRACT"; GOLDEN_REPLAY="GOLDEN_REPLAY"; ONBOARDING_REPORT="ONBOARDING_REPORT"; HANDOFF="HANDOFF"; RECEIPT="RECEIPT"

@dataclass(frozen=True, slots=True)
class Finding:
    code: str; severity: Severity; path: str; message: str; remediation: str; details: dict[str,Any]=field(default_factory=dict)
    def to_dict(self)->dict[str,Any]:
        return {"code":self.code,"severity":self.severity.value,"path":self.path,"message":self.message,"remediation":self.remediation,"details":self.details}

@dataclass(frozen=True, slots=True)
class CompileArtifact:
    artifact_id: str; kind: ArtifactKind; relative_path: str; content_digest: str; source_digest: str; schema_version: str="1.0.0"
    def to_dict(self)->dict[str,Any]:
        return {"artifact_id":self.artifact_id,"kind":self.kind.value,"relative_path":self.relative_path,"content_digest":self.content_digest,"source_digest":self.source_digest,"schema_version":self.schema_version}
