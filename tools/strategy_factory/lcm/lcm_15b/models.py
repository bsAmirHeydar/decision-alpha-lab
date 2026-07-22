from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class VerificationResult:
 root_relocation_count:int
 documentation_relocation_count:int
 revalidated_candidate_count:int
 future_deletion_approved_count:int
 validation_status:str
