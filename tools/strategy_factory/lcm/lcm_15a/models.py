from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class VerificationResult:
    candidate_count:int
    approved_relocation_count:int
    blocked_deletion_count:int
    validation_status:str
