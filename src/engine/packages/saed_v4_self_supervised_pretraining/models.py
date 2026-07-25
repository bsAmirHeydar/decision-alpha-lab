from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .errors import ContractError

ALLOWED_ROLES={"development","training","validation"}
ALLOWED_SPLITS={"train","validation","test","quarantine"}
ALLOWED_OBJECTIVES={
 "masked_span","next_event","temporal_contrast","cross_view_alignment",
 "graph_relation_reconstruction","context_transition","missingness_reconstruction"
}

@dataclass(frozen=True)
class CorpusRecord:
    record_id: str
    context_id: str
    root_context_id: str
    parent_context_id: str|None
    domain_id: str
    event_time: str
    known_time: str
    evidence_role: str
    views: Mapping[str, Mapping[str, Any]]
    graph_relations: tuple[str,...]
    descriptor_tokens: tuple[str,...]
    source_hashes: tuple[str,...]
    synthetic: bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"CorpusRecord":
        required={"record_id","context_id","root_context_id","parent_context_id","domain_id","event_time","known_time","evidence_role","views","graph_relations","descriptor_tokens","source_hashes","synthetic"}
        unknown=set(x)-required
        missing=required-set(x)
        if unknown or missing: raise ContractError(f"corpus record fields unknown={sorted(unknown)} missing={sorted(missing)}")
        obj=cls(str(x['record_id']),str(x['context_id']),str(x['root_context_id']),None if x['parent_context_id'] is None else str(x['parent_context_id']),str(x['domain_id']),str(x['event_time']),str(x['known_time']),str(x['evidence_role']),dict(x['views']),tuple(map(str,x['graph_relations'])),tuple(map(str,x['descriptor_tokens'])),tuple(map(str,x['source_hashes'])),bool(x['synthetic']))
        if obj.evidence_role not in ALLOWED_ROLES: raise ContractError('forbidden evidence role')
        if obj.known_time < obj.event_time: raise ContractError('known_time precedes event_time')
        if not obj.record_id or not obj.context_id or not obj.root_context_id or not obj.domain_id: raise ContractError('identity fields required')
        return obj

@dataclass(frozen=True)
class TokenStream:
    record_id: str
    context_id: str
    root_context_id: str
    domain_id: str
    event_time: str
    known_time: str
    split: str
    tokens: tuple[str,...]
    view_masks: Mapping[str,int]
    token_hash: str

@dataclass(frozen=True)
class ObjectiveSpec:
    objective_id: str
    objective_kind: str
    weight: float
    enabled: bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"ObjectiveSpec":
        obj=cls(str(x['objective_id']),str(x['objective_kind']),float(x['weight']),bool(x['enabled']))
        if obj.objective_kind not in ALLOWED_OBJECTIVES: raise ContractError(f"unknown objective {obj.objective_kind}")
        if obj.weight < 0: raise ContractError('negative objective weight')
        return obj

@dataclass(frozen=True)
class CurriculumStage:
    stage_id: str
    epochs: int
    objective_ids: tuple[str,...]
    max_pairs_per_record: int
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"CurriculumStage":
        obj=cls(str(x['stage_id']),int(x['epochs']),tuple(map(str,x['objective_ids'])),int(x['max_pairs_per_record']))
        if obj.epochs<1 or obj.max_pairs_per_record<1: raise ContractError('invalid curriculum budget')
        return obj

@dataclass(frozen=True)
class TrainingConfig:
    exact_version: str
    seed: int
    embedding_dim: int
    learning_rate: float
    negative_samples: int
    max_total_pairs: int
    deterministic: bool
    objectives: tuple[ObjectiveSpec,...]
    curriculum: tuple[CurriculumStage,...]
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"TrainingConfig":
        required={"exact_version","seed","embedding_dim","learning_rate","negative_samples","max_total_pairs","deterministic","objectives","curriculum"}
        if set(x)!=required: raise ContractError(f"training config fields mismatch: {sorted(set(x)^required)}")
        obj=cls(str(x['exact_version']),int(x['seed']),int(x['embedding_dim']),float(x['learning_rate']),int(x['negative_samples']),int(x['max_total_pairs']),bool(x['deterministic']),tuple(ObjectiveSpec.from_mapping(o) for o in x['objectives']),tuple(CurriculumStage.from_mapping(s) for s in x['curriculum']))
        if not obj.deterministic: raise ContractError('reference trainer must be deterministic')
        if not 4<=obj.embedding_dim<=256: raise ContractError('embedding dimension outside reference range')
        if not 0<obj.learning_rate<=1: raise ContractError('invalid learning rate')
        if not 1<=obj.negative_samples<=32: raise ContractError('invalid negative sample count')
        if obj.max_total_pairs<1: raise ContractError('invalid exposure budget')
        ids=[o.objective_id for o in obj.objectives]
        if len(ids)!=len(set(ids)): raise ContractError('duplicate objective id')
        known=set(ids)
        for stage in obj.curriculum:
            if not set(stage.objective_ids)<=known: raise ContractError('curriculum references unknown objective')
        return obj
