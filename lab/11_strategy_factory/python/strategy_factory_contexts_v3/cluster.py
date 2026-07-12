"""Dependence-aware cluster rule compiler for splits, statistics and treatment siblings."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any
from strategy_factory_contracts_v3 import IdentityKind, build_identity, canonical_sha256
from .enums import ClusterKind
from .lifecycle import ContextObservation
from .errors import ClusterError
from .utils import safe_id, contract_safe

@dataclass(frozen=True, slots=True)
class ClusterRule:
    rule_id: str; version: str; owner_id: str; kind: ClusterKind; dimensions: tuple[str,...]; parameters: Mapping[str,Any]
    def __post_init__(self)->None:
        safe_id(self.rule_id,"rule_id"); safe_id(self.version,"version"); safe_id(self.owner_id,"owner_id")
        if not self.dimensions: raise ClusterError("cluster_without_dimensions","cluster rule requires dimensions")
        if len(set(self.dimensions))!=len(self.dimensions): raise ClusterError("duplicate_cluster_dimension","cluster dimensions contain duplicates")
    def material(self)->Mapping[str,Any]: return {"dimensions":list(self.dimensions),"kind":self.kind.value,"owner_id":self.owner_id,"parameters":contract_safe(self.parameters),"rule_id":self.rule_id,"version":self.version}
    @property
    def rule_hash(self)->str: return canonical_sha256(self.material())

@dataclass(frozen=True, slots=True)
class ClusterAssignment:
    rule_id: str; rule_version: str; cluster_kind: ClusterKind; context_observation_id: str; cluster_id: str; dimensions: Mapping[str,Any]; evidence_hash: str

class ClusterCompiler:
    def compile(self,rule:ClusterRule,observation:ContextObservation,dimensions:Mapping[str,Any])->ClusterAssignment:
        missing=sorted(set(rule.dimensions)-set(dimensions))
        if missing: raise ClusterError("missing_cluster_dimension","cluster dimensions are missing",{"missing":missing,"rule_id":rule.rule_id})
        selected={key:contract_safe(dimensions[key]) for key in sorted(rule.dimensions)}
        material={"context_observation_id":observation.observation_id,"dimensions":selected,"kind":rule.kind.value,"rule_hash":rule.rule_hash,"rule_id":rule.rule_id,"rule_version":rule.version}
        cluster_id=build_identity(IdentityKind.CONTEXT_CLUSTER,namespace="ucee.context_cluster",version=rule.version,owner_id=rule.owner_id,cluster_kind=rule.kind.value,rule_id=rule.rule_id,dimensions=selected).stable_id
        return ClusterAssignment(rule.rule_id,rule.version,rule.kind,observation.observation_id,cluster_id,selected,canonical_sha256(material))
