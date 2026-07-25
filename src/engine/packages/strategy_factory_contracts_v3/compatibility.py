"""Pre-compute compatibility engine with explicit reason codes."""
from __future__ import annotations
from dataclasses import dataclass
from .capability import CapabilityDescriptor
from .enums import CompatibilityStatus,RepresentationKind,RuntimeMode,SupportLevel,TaskType
from .migration import MigrationRegistry
from .schema import SchemaId,SchemaRegistry

@dataclass(frozen=True,slots=True)
class CompatibilityRequest:
    consumer_component_id:str
    context_kind:str
    representation_kind:RepresentationKind
    task_type:TaskType
    treatment_family:str
    runtime_mode:RuntimeMode
    export_target:str
    input_schema:SchemaId
    required_output_schema:SchemaId
    feature_count:int
    sequence_length:int=1
    batch_size:int=1
    estimated_memory_mb:int=1
    latency_budget_us:int=1
    requires_missing_values:bool=False
    requires_sample_weights:bool=False
    requires_multitask:bool=False
    requires_determinism:bool=True
    minimum_support_level:SupportLevel=SupportLevel.RESEARCH

@dataclass(frozen=True,slots=True)
class CompatibilityDecision:
    status:CompatibilityStatus
    reason_codes:tuple[str,...]
    migration_path:tuple[str,...]=()

    @property
    def accepted(self)->bool:return self.status!=CompatibilityStatus.INCOMPATIBLE

class CompatibilityEngine:
    def __init__(self,schemas:SchemaRegistry,migrations:MigrationRegistry)->None:
        self.schemas=schemas;self.migrations=migrations

    def evaluate(self,cap:CapabilityDescriptor,req:CompatibilityRequest)->CompatibilityDecision:
        reasons:list[str]=[]
        def reject(condition:bool,code:str)->None:
            if condition:reasons.append(code)
        reject(req.consumer_component_id!=cap.component_id,"component_id_mismatch")
        support_rank={SupportLevel.EXPERIMENTAL:0,SupportLevel.RESEARCH:1,SupportLevel.PAPER:2,SupportLevel.PRODUCTION:3}
        reject(support_rank[cap.support_level]<support_rank[req.minimum_support_level],"support_level_insufficient")
        reject(req.context_kind not in cap.context_kinds,"context_kind_unsupported")
        reject(req.representation_kind not in cap.representation_kinds,"representation_unsupported")
        reject(req.task_type not in cap.task_types,"task_unsupported")
        reject(req.treatment_family not in cap.treatment_families,"treatment_unsupported")
        reject(req.runtime_mode not in cap.runtime_modes,"runtime_mode_unsupported")
        reject(req.export_target not in cap.export_targets,"export_target_unsupported")
        reject(req.required_output_schema.exact_key not in cap.output_schema_ids,"output_schema_unsupported")
        reject(req.requires_missing_values and not cap.supports_missing_values,"missing_values_unsupported")
        reject(req.requires_sample_weights and not cap.supports_sample_weights,"sample_weights_unsupported")
        reject(req.requires_multitask and not cap.supports_multitask,"multitask_unsupported")
        reject(req.requires_determinism and not cap.deterministic,"determinism_required")
        budget=cap.resource_budget
        reject(req.feature_count>budget.max_features,"feature_budget_exceeded")
        reject(req.sequence_length>budget.max_sequence_length,"sequence_budget_exceeded")
        reject(req.batch_size>budget.max_batch_size,"batch_budget_exceeded")
        reject(req.estimated_memory_mb>budget.max_memory_mb,"memory_budget_exceeded")
        reject(req.latency_budget_us>budget.max_latency_us,"latency_budget_exceeded")
        try:self.schemas.resolve_exact(req.required_output_schema)
        except Exception:reasons.append("required_output_schema_unknown")
        migration_path:tuple[str,...]=()
        if req.input_schema.exact_key in cap.input_schema_ids:
            try:self.schemas.resolve_exact(req.input_schema)
            except Exception:reasons.append("input_schema_unknown")
        else:
            destinations=[]
            for exact in cap.input_schema_ids:
                try:
                    target=self._parse_exact(exact)
                    path=self.migrations.find_path(req.input_schema,target)
                    destinations.append((len(path),exact,path))
                except Exception:continue
            if destinations:
                _,_,selected=min(destinations,key=lambda item:(item[0],item[1]))
                migration_path=tuple(edge.migration_id for edge in selected)
            else:reasons.append("input_schema_unsupported_and_unmigratable")
        if reasons:return CompatibilityDecision(CompatibilityStatus.INCOMPATIBLE,tuple(sorted(set(reasons))))
        if migration_path:return CompatibilityDecision(CompatibilityStatus.COMPATIBLE_AFTER_MIGRATION,(),migration_path)
        return CompatibilityDecision(CompatibilityStatus.COMPATIBLE,())

    @staticmethod
    def _parse_exact(value:str)->SchemaId:
        family,version=value.rsplit("@",1);namespace,name=family.rsplit("/",1)
        from .schema import SemanticVersion
        return SchemaId(namespace,name,SemanticVersion.parse(version))
