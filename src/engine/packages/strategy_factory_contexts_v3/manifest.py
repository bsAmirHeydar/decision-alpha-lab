"""Immutable context package manifest and dependency declarations."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Any
from strategy_factory_contracts_v3 import IdentityKind, build_identity, canonical_sha256
from .enums import ContextUpdateScope, SourceRequirementKind, RequirementStrength, AvailabilityMode, ManualPolicyKind, TaskKind
from .errors import ManifestError
from .utils import safe_id, nonempty_tuple, contract_safe

@dataclass(frozen=True, slots=True)
class SourceRequirement:
    requirement_id: str
    kind: SourceRequirementKind
    strength: RequirementStrength
    symbols: tuple[str,...]
    timeframe_seconds: int=0
    lookback: int=0
    max_staleness_ms: int=0
    synchronization_group_id: str="none"
    purpose: str=""
    def __post_init__(self) -> None:
        safe_id(self.requirement_id,"requirement_id"); safe_id(self.synchronization_group_id,"synchronization_group_id")
        if not self.symbols: raise ManifestError("missing_symbols","source requirement needs at least one symbol")
        if self.timeframe_seconds < 0 or self.lookback < 0 or self.max_staleness_ms < 0: raise ManifestError("negative_requirement_limit","source requirement limits may not be negative")
    def material(self) -> Mapping[str,Any]:
        return {"kind":self.kind.value,"lookback":self.lookback,"max_staleness_ms":self.max_staleness_ms,"purpose":self.purpose,"requirement_id":self.requirement_id,"strength":self.strength.value,"symbols":list(self.symbols),"synchronization_group_id":self.synchronization_group_id,"timeframe_seconds":self.timeframe_seconds}

@dataclass(frozen=True, slots=True)
class ComponentReference:
    component_id: str
    version: str
    schema_hash: str
    required: bool=True
    def __post_init__(self) -> None:
        safe_id(self.component_id,"component_id"); safe_id(self.version,"version"); safe_id(self.schema_hash,"schema_hash")
    def material(self) -> Mapping[str,Any]: return {"component_id":self.component_id,"required":self.required,"schema_hash":self.schema_hash,"version":self.version}

@dataclass(frozen=True, slots=True)
class ManualPolicyReference:
    policy_id: str; version: str; kind: ManualPolicyKind; required_feature_ids: tuple[str,...]=()
    def __post_init__(self) -> None: safe_id(self.policy_id,"policy_id"); safe_id(self.version,"version")
    def material(self) -> Mapping[str,Any]: return {"kind":self.kind.value,"policy_id":self.policy_id,"required_feature_ids":list(self.required_feature_ids),"version":self.version}

@dataclass(frozen=True, slots=True)
class TaskReference:
    task_id: str; version: str; kind: TaskKind; label_contract_id: str; allowed_view_ids: tuple[str,...]
    def __post_init__(self) -> None:
        safe_id(self.task_id,"task_id"); safe_id(self.version,"version"); safe_id(self.label_contract_id,"label_contract_id")
        if not self.allowed_view_ids: raise ManifestError("task_without_view","task must allow at least one representation view",{"task_id":self.task_id})
    def material(self) -> Mapping[str,Any]: return {"allowed_view_ids":list(self.allowed_view_ids),"kind":self.kind.value,"label_contract_id":self.label_contract_id,"task_id":self.task_id,"version":self.version}

@dataclass(frozen=True, slots=True)
class ContextPackageManifest:
    package_id: str
    version: str
    owner_id: str
    doctrine_id: str
    doctrine_version: str
    anatomy_adapter_id: str
    anatomy_adapter_version: str
    update_scope: ContextUpdateScope
    runtime_modes: AvailabilityMode
    source_requirements: tuple[SourceRequirement,...]
    feature_packs: tuple[ComponentReference,...]
    representation_views: tuple[ComponentReference,...]
    cluster_rules: tuple[ComponentReference,...]
    manual_policies: tuple[ManualPolicyReference,...]=()
    tasks: tuple[TaskReference,...]=()
    parent_package_id: str="none"
    description: str=""
    metadata: Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self) -> None:
        for name in ("package_id","version","owner_id","doctrine_id","doctrine_version","anatomy_adapter_id","anatomy_adapter_version","parent_package_id"):
            safe_id(getattr(self,name),name)
        if self.update_scope == ContextUpdateScope.NONE: raise ManifestError("empty_update_scope","context package update_scope is empty")
        if self.runtime_modes == AvailabilityMode.NONE: raise ManifestError("empty_runtime_modes","context package runtime_modes is empty")
        if not self.source_requirements: raise ManifestError("no_sources","context package must declare sources")
        ids=[x.requirement_id for x in self.source_requirements]
        if len(ids)!=len(set(ids)): raise ManifestError("duplicate_source_requirement","source requirement IDs must be unique")
        for refs,field_name in ((self.feature_packs,"feature_packs"),(self.representation_views,"representation_views"),(self.cluster_rules,"cluster_rules")):
            ids=[x.component_id for x in refs]
            if len(ids)!=len(set(ids)): raise ManifestError("duplicate_component",f"{field_name} contains duplicate component IDs")
        unknown=set(self.metadata).intersection({"created_at","updated_at","random","uuid","process_id"})
        if unknown: raise ManifestError("mutable_manifest_metadata","manifest metadata contains mutable fields",{"fields":sorted(unknown)})
    def material(self) -> Mapping[str,Any]:
        return {"anatomy_adapter":{"id":self.anatomy_adapter_id,"version":self.anatomy_adapter_version},"cluster_rules":[x.material() for x in self.cluster_rules],"description":self.description,"doctrine":{"id":self.doctrine_id,"version":self.doctrine_version},"feature_packs":[x.material() for x in self.feature_packs],"manual_policies":[x.material() for x in self.manual_policies],"metadata":contract_safe(self.metadata),"owner_id":self.owner_id,"package_id":self.package_id,"parent_package_id":self.parent_package_id,"representation_views":[x.material() for x in self.representation_views],"runtime_modes":int(self.runtime_modes),"source_requirements":[x.material() for x in self.source_requirements],"tasks":[x.material() for x in self.tasks],"update_scope":int(self.update_scope),"version":self.version}
    @property
    def package_identity(self) -> str:
        return build_identity(IdentityKind.CONTEXT_OCCURRENCE,namespace="ucee.context_package",version=self.version,owner_id=self.owner_id,package_id=self.package_id,manifest_hash=self.manifest_hash).stable_id
    @property
    def manifest_hash(self) -> str: return canonical_sha256(self.material())
