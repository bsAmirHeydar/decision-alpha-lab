from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class VerificationResult:
 candidate_count:int
 approved_deletion_count:int
 deleted_path_count:int
 blocked_path_count:int
 clean_clone_status:str
 archive_restore_status:str
 validation_status:str
