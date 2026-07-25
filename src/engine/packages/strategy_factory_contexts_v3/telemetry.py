"""Bounded counters for context package runtime and conformance operations."""
from dataclasses import dataclass
@dataclass(slots=True)
class ContextTelemetry:
    source_records:int=0; observations_emitted:int=0; duplicates_suppressed:int=0; transitions:int=0; invalid_transitions:int=0; feature_frames:int=0; missing_features:int=0; stale_features:int=0; views_compiled:int=0; view_failures:int=0; clusters_assigned:int=0; conformance_failures:int=0
    def material(self): return {k:getattr(self,k) for k in self.__dataclass_fields__}
