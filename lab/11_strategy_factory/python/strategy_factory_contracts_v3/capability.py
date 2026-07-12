"""Machine-readable provider/consumer capability descriptors."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .enums import RepresentationKind,RuntimeMode,SupportLevel,TaskType
from .validation import require_safe_identifier,require_unique

@dataclass(frozen=True,slots=True)
class ResourceBudget:
    max_features:int
    max_sequence_length:int
    max_batch_size:int
    max_memory_mb:int
    max_latency_us:int

    def __post_init__(self)->None:
        for name,value in (("max_features",self.max_features),("max_sequence_length",self.max_sequence_length),("max_batch_size",self.max_batch_size),("max_memory_mb",self.max_memory_mb),("max_latency_us",self.max_latency_us)):
            if not isinstance(value,int) or isinstance(value,bool) or value<=0: raise ValueError(f"{name} must be a positive integer")

@dataclass(frozen=True,slots=True)
class CapabilityDescriptor:
    component_id:str
    component_version:str
    support_level:SupportLevel
    context_kinds:tuple[str,...]
    representation_kinds:tuple[RepresentationKind,...]
    task_types:tuple[TaskType,...]
    treatment_families:tuple[str,...]
    runtime_modes:tuple[RuntimeMode,...]
    export_targets:tuple[str,...]
    input_schema_ids:tuple[str,...]
    output_schema_ids:tuple[str,...]
    supports_missing_values:bool
    supports_sample_weights:bool
    supports_multitask:bool
    deterministic:bool
    resource_budget:ResourceBudget

    def __post_init__(self)->None:
        require_safe_identifier(self.component_id,"component_id")
        require_safe_identifier(self.component_version,"component_version")
        for field_name,values in (("context_kinds",self.context_kinds),("treatment_families",self.treatment_families),("export_targets",self.export_targets),("input_schema_ids",self.input_schema_ids),("output_schema_ids",self.output_schema_ids)):
            require_unique(values,field_name)
        if not self.input_schema_ids or not self.output_schema_ids: raise ValueError("capability requires exact input and output schemas")

    def supports_all(self,values:Iterable[object],supported:Iterable[object])->bool:
        return set(values).issubset(set(supported))
