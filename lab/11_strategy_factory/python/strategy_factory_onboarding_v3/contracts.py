from __future__ import annotations
import math,re
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import canonical_sha256,safe_relative_path
from .enums import *
from .errors import OnboardingError
SHA=re.compile(r'^[0-9a-f]{64}$');SEMVER=re.compile(r'^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$');IDENT=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:@/-]*$')
def _id(v,n):
    if not isinstance(v,str) or not IDENT.fullmatch(v):raise OnboardingError('invalid_identifier',f'{n} invalid',{'value':v})
def _hash(v,n):
    if not isinstance(v,str) or not SHA.fullmatch(v):raise OnboardingError('invalid_hash',f'{n} must be lowercase sha256')
def _ver(v,n):
    if not isinstance(v,str) or not SEMVER.fullmatch(v):raise OnboardingError('invalid_semver',f'{n} invalid')
def _uniq(values,n):
    if not values or len(values)!=len(set(values)):raise OnboardingError('invalid_unique_list',f'{n} must be unique and non-empty')

@dataclass(frozen=True,slots=True)
class FeatureSpec:
    feature_id:str;dtype:str;known_time_rule:str;required:bool=True;default:Any=None;description:str=''
    def __post_init__(self):
        _id(self.feature_id,'feature_id');_id(self.dtype,'dtype');_id(self.known_time_rule,'known_time_rule')
        if self.dtype not in {'float','int','bool','string','category'}:raise OnboardingError('unsupported_dtype','unsupported feature dtype')
    @property
    def spec_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ViewSpec:
    view_id:str;feature_ids:tuple[str,...];shape:tuple[int,...];causal:bool=True;optional:bool=False
    def __post_init__(self):
        _id(self.view_id,'view_id');_uniq(self.feature_ids,'feature_ids')
        if not self.shape or any(int(x)<1 for x in self.shape):raise OnboardingError('invalid_shape','shape must be positive')
        if not self.causal:raise OnboardingError('non_causal_view','onboarding views must be causal')

@dataclass(frozen=True,slots=True)
class CapabilityDeclaration:
    capability_id:str;decision:CapabilityDecision;reason:str;scope:str='context'
    def __post_init__(self):
        _id(self.capability_id,'capability_id');_id(self.scope,'scope')
        if self.decision is CapabilityDecision.DECLARED_EXCEPTION and not self.reason.strip():raise OnboardingError('missing_exception_reason','exception requires reason')

@dataclass(frozen=True,slots=True)
class ContextSpecification:
    context_id:str;version:str;display_name:str;kind:ContextKind;wave:MigrationWave;doctrine_hash:str;source_hashes:tuple[str,...];features:tuple[FeatureSpec,...];views:tuple[ViewSpec,...];lifecycle_states:tuple[str,...];cluster_rule_ids:tuple[str,...];task_ids:tuple[str,...];manual_policy_id:str;capabilities:tuple[CapabilityDeclaration,...];legacy_source_paths:tuple[str,...]=();exception_ids:tuple[str,...]=()
    def __post_init__(self):
        _id(self.context_id,'context_id');_ver(self.version,'version');_hash(self.doctrine_hash,'doctrine_hash');_id(self.manual_policy_id,'manual_policy_id')
        _uniq(tuple(x.feature_id for x in self.features),'features');_uniq(tuple(x.view_id for x in self.views),'views');_uniq(self.lifecycle_states,'lifecycle_states');_uniq(self.cluster_rule_ids,'cluster_rule_ids');_uniq(self.task_ids,'task_ids');_uniq(tuple(x.capability_id for x in self.capabilities),'capabilities')
        for h in self.source_hashes:_hash(h,'source_hash')
        feature_ids={x.feature_id for x in self.features}
        for view in self.views:
            missing=set(view.feature_ids)-feature_ids
            if missing:raise OnboardingError('unknown_view_feature','view references unknown feature',{'missing':sorted(missing)})
        for p in self.legacy_source_paths:safe_relative_path(p)
    @property
    def spec_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class GeneratedArtifact:
    path:str;content_hash:str;kind:str;identity_relevant:bool=True
    def __post_init__(self):safe_relative_path(self.path);_hash(self.content_hash,'content_hash');_id(self.kind,'kind')

@dataclass(frozen=True,slots=True)
class ScaffoldManifest:
    manifest_id:str;version:str;context_id:str;context_spec_hash:str;generator_version:str;artifacts:tuple[GeneratedArtifact,...];tournament_template_hash:str;core_snapshot_hash:str
    def __post_init__(self):
        _id(self.manifest_id,'manifest_id');_ver(self.version,'version');_id(self.context_id,'context_id');_ver(self.generator_version,'generator_version')
        for n in ('context_spec_hash','tournament_template_hash','core_snapshot_hash'):_hash(getattr(self,n),n)
        paths=[a.path for a in self.artifacts]
        if not paths or len(paths)!=len(set(paths)):raise OnboardingError('duplicate_artifact_path','artifact paths unique and non-empty')
    @property
    def manifest_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class LegacyAdapterSpec:
    adapter_id:str;version:str;context_id:str;source_paths:tuple[str,...];source_hashes:tuple[str,...];mode:AdapterMode;shared_treatment_path:bool;shared_economics_path:bool;shared_validation_path:bool;shared_runtime_path:bool;mutation_isolated:bool;exception_ids:tuple[str,...]=()
    def __post_init__(self):
        _id(self.adapter_id,'adapter_id');_ver(self.version,'version');_id(self.context_id,'context_id');_uniq(self.source_paths,'source_paths')
        for p in self.source_paths:safe_relative_path(p)
        for h in self.source_hashes:_hash(h,'source_hash')
        if len(self.source_hashes)!=len(self.source_paths):raise OnboardingError('source_hash_count_mismatch','source hashes must align')
        if not all((self.shared_treatment_path,self.shared_economics_path,self.shared_validation_path,self.shared_runtime_path)):raise OnboardingError('shared_path_bypass','legacy adapter cannot bypass shared paths')
        if not self.mutation_isolated:raise OnboardingError('mutation_not_isolated','legacy mutations must be isolated')
    @property
    def spec_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class DifferentialObservation:
    observation_id:str;known_time_ms:int;legacy_output:Mapping[str,Any];canonical_output:Mapping[str,Any];field_deltas:Mapping[str,float];matched:bool;reason:str='none'
    def __post_init__(self):
        _id(self.observation_id,'observation_id');_id(self.reason,'reason')
        for v in self.field_deltas.values():
            if not math.isfinite(float(v)) or float(v)<0:raise OnboardingError('invalid_delta','delta must be finite non-negative')

@dataclass(frozen=True,slots=True)
class DifferentialParityReport:
    report_id:str;version:str;adapter_hash:str;observations:tuple[DifferentialObservation,...];status:ParityStatus;matched_count:int;mismatch_count:int;max_delta:float;tolerance:float;behavior_change_allowed:bool=False
    def __post_init__(self):
        _id(self.report_id,'report_id');_ver(self.version,'version');_hash(self.adapter_hash,'adapter_hash')
        if self.matched_count+self.mismatch_count!=len(self.observations):raise OnboardingError('parity_count_mismatch','parity counts mismatch')
        if self.status is ParityStatus.PASS and self.mismatch_count:raise OnboardingError('false_parity_pass','pass cannot contain mismatches')
        if self.behavior_change_allowed and self.status is not ParityStatus.PASS:raise OnboardingError('change_before_parity','behavior changes require measured parity first')
    @property
    def report_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class MigrationUnit:
    unit_id:str;context_id:str;wave:MigrationWave;adapter_hash:str;spec_hash:str;source_family:str;capability_hash:str;status:MigrationStatus;dependencies:tuple[str,...]=();limitations:tuple[str,...]=()
    def __post_init__(self):
        for n in ('unit_id','context_id','source_family'):_id(getattr(self,n),n)
        for n in ('adapter_hash','spec_hash','capability_hash'):_hash(getattr(self,n),n)

@dataclass(frozen=True,slots=True)
class MigrationWavePlan:
    plan_id:str;version:str;wave:MigrationWave;units:tuple[MigrationUnit,...];stop_after_unit:str|None=None;core_snapshot_hash:str='0'*64
    def __post_init__(self):
        _id(self.plan_id,'plan_id');_ver(self.version,'version');_hash(self.core_snapshot_hash,'core_snapshot_hash');_uniq(tuple(x.unit_id for x in self.units),'units')
        if any(x.wave is not self.wave for x in self.units):raise OnboardingError('wave_mismatch','all units must match wave')
        if self.stop_after_unit is not None and self.stop_after_unit not in {x.unit_id for x in self.units}:raise OnboardingError('unknown_stop_unit','stop unit not in plan')
    @property
    def plan_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class MigrationWaveReport:
    report_id:str;version:str;plan_hash:str;completed_unit_ids:tuple[str,...];stopped:bool;failed_unit_id:str|None;unaffected_context_ids:tuple[str,...];core_invariant:bool
    def __post_init__(self):
        _id(self.report_id,'report_id');_ver(self.version,'version');_hash(self.plan_hash,'plan_hash')
        if not self.core_invariant:raise OnboardingError('core_changed_during_migration','migration changed central engine')
    @property
    def report_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class TournamentTemplateSpec:
    template_id:str;version:str;context_spec_hash:str;data_cut_policy_id:str;treatment_freeze_policy_id:str;trainer_budget_id:str;search_budget_id:str;anti_overfit_policy_id:str;paper_policy_id:str;runtime_policy_id:str;promotion_policy_id:str;seed:int
    def __post_init__(self):
        _id(self.template_id,'template_id');_ver(self.version,'version');_hash(self.context_spec_hash,'context_spec_hash')
        for n in ('data_cut_policy_id','treatment_freeze_policy_id','trainer_budget_id','search_budget_id','anti_overfit_policy_id','paper_policy_id','runtime_policy_id','promotion_policy_id'):_id(getattr(self,n),n)
        if self.seed<0:raise OnboardingError('negative_seed','seed non-negative')
    @property
    def template_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CompiledTournamentTemplate:
    compiled_id:str;version:str;template_hash:str;stage_ids:tuple[str,...];artifact_identity_map:Mapping[str,str];final_test_sealed:bool=True;fixture_not_alpha_proof:bool=True
    def __post_init__(self):
        _id(self.compiled_id,'compiled_id');_ver(self.version,'version');_hash(self.template_hash,'template_hash');_uniq(self.stage_ids,'stage_ids')
        for h in self.artifact_identity_map.values():_hash(h,'artifact_identity')
        if not self.final_test_sealed:raise OnboardingError('unsealed_final_test','final test must remain sealed')
        if not self.fixture_not_alpha_proof:raise OnboardingError('fixture_claimed_as_alpha','fixture cannot prove alpha')
    @property
    def compiled_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CoreSnapshot:
    snapshot_id:str;version:str;root_hash:str;file_hashes:Mapping[str,str];captured_at_ms:int=0
    def __post_init__(self):
        _id(self.snapshot_id,'snapshot_id');_ver(self.version,'version');_hash(self.root_hash,'root_hash')
        for p,h in self.file_hashes.items():safe_relative_path(p);_hash(h,'file_hash')
    @property
    def snapshot_hash(self):return canonical_sha256({'version':self.version,'root_hash':self.root_hash,'file_hashes':self.file_hashes})

@dataclass(frozen=True,slots=True)
class EngineInvarianceReport:
    report_id:str;version:str;before_hash:str;after_hash:str;status:InvarianceStatus;changed_core_paths:tuple[str,...];allowed_plugin_paths:tuple[str,...];adr_id:str|None=None;compatibility_review_hash:str|None=None
    def __post_init__(self):
        _id(self.report_id,'report_id');_ver(self.version,'version');_hash(self.before_hash,'before_hash');_hash(self.after_hash,'after_hash')
        for p in self.changed_core_paths+self.allowed_plugin_paths:safe_relative_path(p)
        if self.status is InvarianceStatus.PASS and self.changed_core_paths:raise OnboardingError('false_invariance_pass','pass cannot include changed core paths')
        if self.changed_core_paths and self.status is not InvarianceStatus.ADR_REQUIRED:raise OnboardingError('core_change_without_adr_gate','core changes require ADR gate')
        if self.status is InvarianceStatus.ADR_REQUIRED and (not self.adr_id or not self.compatibility_review_hash):raise OnboardingError('missing_adr_evidence','ADR and compatibility review required')
        if self.compatibility_review_hash:_hash(self.compatibility_review_hash,'compatibility_review_hash')
    @property
    def report_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class OnboardingEvidenceBundle:
    bundle_id:str;version:str;manifest_hash:str;parity_report_hashes:tuple[str,...];migration_report_hashes:tuple[str,...];invariance_report_hash:str;test_evidence_hash:str;limitations:tuple[str,...];next_phase:str
    def __post_init__(self):
        _id(self.bundle_id,'bundle_id');_ver(self.version,'version');_hash(self.manifest_hash,'manifest_hash');_hash(self.invariance_report_hash,'invariance_report_hash');_hash(self.test_evidence_hash,'test_evidence_hash');_id(self.next_phase,'next_phase')
        for h in self.parity_report_hashes+self.migration_report_hashes:_hash(h,'evidence_hash')
    @property
    def bundle_hash(self):return canonical_sha256(asdict(self))
