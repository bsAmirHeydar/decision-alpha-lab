from __future__ import annotations
from dataclasses import dataclass,asdict
from .canonical import canonical_sha256
@dataclass(frozen=True,slots=True)
class OnboardingTelemetry:
    context_id:str;generated_file_count:int;parity_observation_count:int;migration_unit_count:int;core_changed_count:int;failure_codes:tuple[str,...]=()
    @property
    def telemetry_hash(self):return canonical_sha256(asdict(self))
