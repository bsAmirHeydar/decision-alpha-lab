from __future__ import annotations
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import content_hash,stable_id
from .enums import TwinState,SupportStatus,HypothesisStatus,ContradictionSeverity,DebtSeverity,ObservationKind,RelationKind,TransitionDisposition

@dataclass(frozen=True)
class ContextSpecificationRef:
    context_id:str; context_version:str; artifact_id:str; specification_hash:str; ucee_phase:str; schema_version:str
    def to_dict(self):return asdict(self)

@dataclass(frozen=True)
class TwinSeedRef:
    package_id:str; package_hash:str; lineage_root:str; known_as_of:str; constitution_hash:str; snapshot_ids:tuple[str,...]; schema_versions:Mapping[str,str]; limitations:tuple[str,...]=()
    def to_dict(self):return {**asdict(self),'snapshot_ids':list(self.snapshot_ids),'schema_versions':dict(self.schema_versions),'limitations':list(self.limitations)}

@dataclass(frozen=True)
class OntologyTerm:
    term_id:str; name:str; definition:str; namespace:str; canonical:bool=False; source_ref:str=''
    @property
    def term_hash(self):return content_hash(asdict(self))

@dataclass(frozen=True)
class OntologyRelation:
    source_term_id:str; target_term_id:str; relation_kind:RelationKind; source_ref:str=''
    @property
    def relation_id(self):return stable_id('orel',{'source':self.source_term_id,'target':self.target_term_id,'kind':self.relation_kind.value,'source_ref':self.source_ref})

@dataclass(frozen=True)
class ObservableDefinition:
    observable_id:str; name:str; value_type:str; required:bool; canonical_source:bool; unit:str|None=None; allowed_values:tuple[str,...]=(); minimum:float|None=None; maximum:float|None=None; freshness_seconds:int|None=None
    def to_dict(self):return {**asdict(self),'allowed_values':list(self.allowed_values)}

@dataclass(frozen=True)
class Observation:
    twin_id:str; observable_id:str; value:Any; event_time:str; known_time:str; source_artifact_id:str; source_hash:str; observation_kind:ObservationKind; quality:float=1.0; sequence:int=1
    @property
    def observation_id(self):return stable_id('obs',asdict(self))
    @property
    def observation_hash(self):return content_hash(asdict(self))

@dataclass(frozen=True)
class LatentHypothesis:
    hypothesis_id:str; name:str; description:str; prior_weight:float; scope:str; falsification_rule:str; source_ref:str
    @property
    def hypothesis_hash(self):return content_hash(asdict(self))

@dataclass(frozen=True)
class HypothesisAssessment:
    twin_id:str; hypothesis_id:str; evidence_hash:str; known_time:str; score:float; weight:float; assessor_id:str; rationale:str
    @property
    def assessment_id(self):return stable_id('hassess',asdict(self))

@dataclass(frozen=True)
class HypothesisState:
    hypothesis_id:str; weighted_score:float; total_weight:float; status:HypothesisStatus; assessment_ids:tuple[str,...]

@dataclass(frozen=True)
class SupportDimension:
    dimension_id:str; observable_id:str; required:bool; allowed_values:tuple[str,...]=(); minimum:float|None=None; maximum:float|None=None; maximum_age_seconds:int|None=None; weight:float=1.0

@dataclass(frozen=True)
class SupportGeometry:
    geometry_id:str; dimensions:tuple[SupportDimension,...]; minimum_coverage:float; unknown_policy:str; degraded_threshold:float
    @property
    def geometry_hash(self):return content_hash({'geometry_id':self.geometry_id,'dimensions':[asdict(x) for x in self.dimensions],'minimum_coverage':self.minimum_coverage,'unknown_policy':self.unknown_policy,'degraded_threshold':self.degraded_threshold})

@dataclass(frozen=True)
class SupportEvaluation:
    twin_id:str; geometry_id:str; known_as_of:str; status:SupportStatus; coverage:float; failed_dimensions:tuple[str,...]; unknown_dimensions:tuple[str,...]; reasons:tuple[str,...]
    @property
    def evaluation_id(self):return stable_id('support',asdict(self))

@dataclass(frozen=True)
class LifecycleStateDefinition:
    state_id:str; terminal:bool=False; description:str=''

@dataclass(frozen=True)
class TransitionRule:
    rule_id:str; from_state:str; to_state:str; trigger:str; required_observables:tuple[str,...]=(); forbidden_contradiction_severities:tuple[str,...]=(); requires_support:bool=False; review_required:bool=False

@dataclass(frozen=True)
class TransitionEvent:
    twin_id:str; rule_id:str; from_state:str; to_state:str; known_time:str; trigger:str; evidence_hashes:tuple[str,...]; disposition:TransitionDisposition; reasons:tuple[str,...]; sequence:int
    @property
    def event_id(self):return stable_id('ttrans',asdict(self))

@dataclass(frozen=True)
class Contradiction:
    twin_id:str; contradiction_key:str; left_hash:str; right_hash:str; severity:ContradictionSeverity; known_time:str; description:str; resolved:bool=False; resolution_hash:str|None=None
    @property
    def contradiction_id(self):return stable_id('contra',asdict(self))

@dataclass(frozen=True)
class EvidenceDebtItem:
    twin_id:str; debt_key:str; description:str; severity:DebtSeverity; source_ref:str; opened_known_time:str; resolved:bool=False; resolution_hash:str|None=None
    @property
    def debt_id(self):return stable_id('debt',asdict(self))

@dataclass(frozen=True)
class TwinAuthorityBoundary:
    read_ucee_truth:bool=True; compile_twin:bool=True; append_observation:bool=True; append_hypothesis_assessment:bool=True; transition_twin:bool=True; mutate_ucee_truth:bool=False; select_treatment:bool=False; allocate_risk:bool=False; activate_runtime:bool=False; send_order:bool=False; network_access:bool=False
    def to_dict(self):return asdict(self)

@dataclass(frozen=True)
class ContextTwinManifest:
    twin_id:str; exact_version:str; compiler_version:str; context_ref:ContextSpecificationRef; seed_ref:TwinSeedRef; ontology_terms:tuple[OntologyTerm,...]; ontology_relations:tuple[OntologyRelation,...]; observables:tuple[ObservableDefinition,...]; hypotheses:tuple[LatentHypothesis,...]; support_geometry:SupportGeometry; lifecycle_states:tuple[LifecycleStateDefinition,...]; transition_rules:tuple[TransitionRule,...]; initial_lifecycle_state:str; twin_state:TwinState; authority:TwinAuthorityBoundary; limitations:tuple[str,...]; semantic_hash:str
    def semantic_payload(self):
        return {'twin_id':self.twin_id,'exact_version':self.exact_version,'compiler_version':self.compiler_version,'context_ref':self.context_ref.to_dict(),'seed_ref':self.seed_ref.to_dict(),'ontology_terms':[asdict(x) for x in self.ontology_terms],'ontology_relations':[{**asdict(x),'relation_kind':x.relation_kind.value} for x in self.ontology_relations],'observables':[x.to_dict() for x in self.observables],'hypotheses':[asdict(x) for x in self.hypotheses],'support_geometry':{'geometry_id':self.support_geometry.geometry_id,'dimensions':[asdict(x) for x in self.support_geometry.dimensions],'minimum_coverage':self.support_geometry.minimum_coverage,'unknown_policy':self.support_geometry.unknown_policy,'degraded_threshold':self.support_geometry.degraded_threshold},'lifecycle_states':[asdict(x) for x in self.lifecycle_states],'transition_rules':[asdict(x) for x in self.transition_rules],'initial_lifecycle_state':self.initial_lifecycle_state,'twin_state':self.twin_state.value,'authority':self.authority.to_dict(),'limitations':list(self.limitations)}

@dataclass(frozen=True)
class TwinStateSnapshot:
    twin_id:str; manifest_hash:str; known_as_of:str; lifecycle_state:str; twin_state:TwinState; observation_ids:tuple[str,...]; hypothesis_states:tuple[HypothesisState,...]; support_evaluation_id:str|None; contradiction_ids:tuple[str,...]; evidence_debt_ids:tuple[str,...]; transition_event_ids:tuple[str,...]; sequence:int; snapshot_hash:str

@dataclass(frozen=True)
class TwinDiff:
    twin_id:str; left_snapshot_hash:str; right_snapshot_hash:str; changed_fields:tuple[str,...]; added_observations:tuple[str,...]; removed_observations:tuple[str,...]; added_contradictions:tuple[str,...]; resolved_contradictions:tuple[str,...]; lifecycle_changed:bool
    @property
    def diff_id(self):return stable_id('tdiff',asdict(self))

@dataclass(frozen=True)
class TwinIntegrityReceipt:
    twin_id:str; manifest_hash:str; state_snapshot_hash:str; component_root:str; status:str; details:Mapping[str,Any]=field(default_factory=dict)
    @property
    def receipt_id(self):return stable_id('treceipt',asdict(self))
