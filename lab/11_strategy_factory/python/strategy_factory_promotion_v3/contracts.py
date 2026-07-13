"""Immutable machine-readable contracts for UCE-I12.

The complete I11 selection universe remains visible.  Missing, failed, skipped,
pruned, cancelled and manually-overridden choices are first-class evidence and
participate in multiplicity counts even when no p-value exists.
"""
from __future__ import annotations
import math, re
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping
from .canonical import canonical_sha256, stable_id
from .enums import CorrectionMethod, DecisionRole, EvidenceStatus, GateOutcome, NullKind, Severity, StressKind, TrialDisposition
from .errors import PromotionError
_SHA=re.compile(r"^[0-9a-f]{64}$")
_SEMVER=re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
_ID=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]*$")

def _text(v:str,n:str)->None:
    if not isinstance(v,str) or not v.strip(): raise PromotionError("required_text_missing", f"{n} is required")
def _id(v:str,n:str)->None:
    _text(v,n)
    if not _ID.match(v): raise PromotionError("invalid_identifier", f"{n} contains unsupported characters", {"value":v})
def _hash(v:str,n:str)->None:
    if not isinstance(v,str) or not _SHA.match(v): raise PromotionError("invalid_sha256", f"{n} must be lowercase SHA-256", {"value":v})
def _semver(v:str,n:str)->None:
    if not isinstance(v,str) or not _SEMVER.match(v): raise PromotionError("invalid_semver", f"{n} must be semantic version")
def _prob(v:float,n:str)->None:
    if not math.isfinite(float(v)) or not 0.0 <= float(v) <= 1.0: raise PromotionError("invalid_probability", f"{n} must be in [0,1]")
def _finite(v:float,n:str)->None:
    if not math.isfinite(float(v)): raise PromotionError("non_finite_value", f"{n} must be finite")

@dataclass(frozen=True, slots=True)
class TrialEvidence:
    trial_id: str
    family_id: str
    candidate_key: str
    task_key: str
    trainer_key: str
    treatment_key: str
    threshold_key: str
    disposition: TrialDisposition
    ledger_entry_hash: str
    p_value: float | None = None
    score: float | None = None
    fold_id: str = ""
    seed: int = 0
    selected: bool = False
    ensembled: bool = False
    manual_override: bool = False
    integrity_blockers: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    def __post_init__(self)->None:
        for n in ("trial_id","family_id","candidate_key","task_key","trainer_key","treatment_key","threshold_key"): _id(getattr(self,n),n)
        _hash(self.ledger_entry_hash,"ledger_entry_hash")
        if self.p_value is not None: _prob(self.p_value,"p_value")
        if self.score is not None: _finite(self.score,"score")
        if self.seed < 0: raise PromotionError("negative_seed","seed must be non-negative")
        if self.selected and self.disposition not in (TrialDisposition.SELECTED, TrialDisposition.ENSEMBLED, TrialDisposition.MANUAL_OVERRIDE):
            raise PromotionError("selected_disposition_mismatch","selected flag requires selected/ensembled/manual_override disposition")
        if self.ensembled and self.disposition is not TrialDisposition.ENSEMBLED: raise PromotionError("ensemble_disposition_mismatch","ensembled flag requires ensembled disposition")
        if self.manual_override and self.disposition is not TrialDisposition.MANUAL_OVERRIDE: raise PromotionError("override_disposition_mismatch","manual override flag requires manual_override disposition")
    @property
    def family_coordinates(self)->tuple[str,...]: return (self.family_id,self.task_key,self.trainer_key,self.treatment_key,self.threshold_key)
    @property
    def evidence_hash(self)->str: return canonical_sha256(asdict(self))

@dataclass(frozen=True, slots=True)
class SelectionUniverse:
    universe_id: str
    universe_version: str
    experiment_manifest_hash: str
    selection_ledger_hash: str
    dataset_hash: str
    split_hash: str
    target_hash: str
    economics_hash: str
    known_time_hash: str
    trials: tuple[TrialEvidence, ...]
    declared_trial_count: int
    ledger_complete: bool = True
    def __post_init__(self)->None:
        _id(self.universe_id,"universe_id"); _semver(self.universe_version,"universe_version")
        for n in ("experiment_manifest_hash","selection_ledger_hash","dataset_hash","split_hash","target_hash","economics_hash","known_time_hash"): _hash(getattr(self,n),n)
        if self.declared_trial_count < 1: raise PromotionError("empty_declared_universe","declared_trial_count must be positive")
        if len(self.trials) != self.declared_trial_count: raise PromotionError("trial_universe_count_mismatch","all declared choices must appear in trials", {"declared":self.declared_trial_count,"actual":len(self.trials)})
        ids=[t.trial_id for t in self.trials]
        if len(set(ids)) != len(ids): raise PromotionError("duplicate_trial_id","trial ids must be unique")
        if not self.ledger_complete: raise PromotionError("incomplete_selection_ledger","incomplete ledger blocks statistical evaluation")
    @property
    def universe_hash(self)->str: return canonical_sha256(asdict(self))
    def disposition_counts(self)->dict[str,int]:
        return {d.value:sum(t.disposition is d for t in self.trials) for d in TrialDisposition}

@dataclass(frozen=True, slots=True)
class FamilyDefinition:
    family_definition_id: str
    dimensions: tuple[str,...] = ("family_id","task_key","trainer_key","treatment_key","threshold_key")
    correction: CorrectionMethod = CorrectionMethod.BENJAMINI_YEKUTIELY
    alpha: float = 0.05
    include_missing_p_values: bool = True
    def __post_init__(self)->None:
        _id(self.family_definition_id,"family_definition_id"); _prob(self.alpha,"alpha")
        allowed={"family_id","task_key","trainer_key","treatment_key","threshold_key","candidate_key","fold_id","seed"}
        if not self.dimensions or set(self.dimensions)-allowed: raise PromotionError("invalid_family_dimensions","unknown or empty family dimensions")
        if len(set(self.dimensions))!=len(self.dimensions): raise PromotionError("duplicate_family_dimension","dimensions must be unique")

@dataclass(frozen=True, slots=True)
class TestEvidence:
    __test__ = False
    test_id: str
    family: str
    status: EvidenceStatus
    severity: Severity
    metric_name: str
    metric_value: float | None
    threshold: float | None
    evidence_hash: str
    blockers: tuple[str,...]=()
    warnings: tuple[str,...]=()
    details: Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self)->None:
        _id(self.test_id,"test_id"); _id(self.family,"family"); _id(self.metric_name,"metric_name"); _hash(self.evidence_hash,"evidence_hash")
        if self.metric_value is not None: _finite(self.metric_value,"metric_value")
        if self.threshold is not None: _finite(self.threshold,"threshold")
        if self.status is EvidenceStatus.FAIL and not self.blockers: raise PromotionError("failed_test_without_blocker","failed evidence requires blocker")
        if self.status is EvidenceStatus.PASS and self.blockers: raise PromotionError("passed_test_with_blocker","passing evidence cannot have blockers")

@dataclass(frozen=True, slots=True)
class UncertaintyReport:
    report_id: str
    estimate: float
    lower: float
    upper: float
    standard_error: float
    nominal_sample_size: int
    effective_sample_size: float
    method: str
    confidence: float
    seed: int
    evidence_hash: str
    subgroup_reports: Mapping[str,Mapping[str,float]]=field(default_factory=dict)
    def __post_init__(self)->None:
        _id(self.report_id,"report_id"); _hash(self.evidence_hash,"evidence_hash"); _prob(self.confidence,"confidence")
        for n in ("estimate","lower","upper","standard_error","effective_sample_size"): _finite(getattr(self,n),n)
        if self.nominal_sample_size<1 or not 0 < self.effective_sample_size <= self.nominal_sample_size: raise PromotionError("invalid_effective_sample_size","ESS must be in (0,n]")
        if self.lower>self.upper: raise PromotionError("inverted_interval","lower exceeds upper")

@dataclass(frozen=True, slots=True)
class MultiplicityReport:
    report_id: str
    universe_hash: str
    family_definition_hash: str
    total_choice_count: int
    tested_choice_count: int
    missing_p_value_count: int
    rejected_trial_ids: tuple[str,...]
    adjusted_p_values: Mapping[str,float]
    family_counts: Mapping[str,int]
    evidence_hash: str
    def __post_init__(self)->None:
        _id(self.report_id,"report_id")
        for n in ("universe_hash","family_definition_hash","evidence_hash"): _hash(getattr(self,n),n)
        if self.total_choice_count<1 or self.tested_choice_count<0 or self.missing_p_value_count<0: raise PromotionError("invalid_multiplicity_counts","invalid multiplicity counts")
        if self.tested_choice_count+self.missing_p_value_count != self.total_choice_count: raise PromotionError("multiplicity_count_mismatch","tested + missing must equal total")
        for v in self.adjusted_p_values.values(): _prob(v,"adjusted_p_value")

@dataclass(frozen=True, slots=True)
class NullControlResult:
    control_id: str
    kind: NullKind
    observed_metric: float
    null_metric: float
    uplift: float
    p_value: float
    status: EvidenceStatus
    sample_count: int
    evidence_hash: str
    details: Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self)->None:
        _id(self.control_id,"control_id"); _hash(self.evidence_hash,"evidence_hash"); _prob(self.p_value,"p_value")
        for n in ("observed_metric","null_metric","uplift"): _finite(getattr(self,n),n)
        if self.sample_count<1: raise PromotionError("empty_null_control","null control sample cannot be empty")

@dataclass(frozen=True, slots=True)
class StressResult:
    stress_id: str
    kind: StressKind
    baseline_metric: float
    stressed_metric: float
    relative_retention: float
    status: EvidenceStatus
    evidence_hash: str
    details: Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self)->None:
        _id(self.stress_id,"stress_id"); _hash(self.evidence_hash,"evidence_hash")
        for n in ("baseline_metric","stressed_metric","relative_retention"): _finite(getattr(self,n),n)

@dataclass(frozen=True, slots=True)
class CalibrationReport:
    report_id: str
    brier_score: float
    log_loss: float
    expected_calibration_error: float
    conformal_coverage: float
    target_coverage: float
    decision_net_benefit: float
    abstention_coverage: float
    risk_tier_error: float
    evidence_hash: str
    details: Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self)->None:
        _id(self.report_id,"report_id"); _hash(self.evidence_hash,"evidence_hash")
        for n in ("brier_score","log_loss","expected_calibration_error","decision_net_benefit","risk_tier_error"): _finite(getattr(self,n),n)
        for n in ("conformal_coverage","target_coverage","abstention_coverage"): _prob(getattr(self,n),n)

@dataclass(frozen=True, slots=True)
class ProspectiveChallengeFreeze:
    challenge_id: str
    challenge_version: str
    declaration_hash: str
    frozen_before_observation: bool
    start_known_time_ms: int
    end_known_time_ms: int
    required_sample_count: int
    decision_rule_hash: str
    def __post_init__(self)->None:
        _id(self.challenge_id,"challenge_id"); _semver(self.challenge_version,"challenge_version")
        _hash(self.declaration_hash,"declaration_hash"); _hash(self.decision_rule_hash,"decision_rule_hash")
        if not self.frozen_before_observation: raise PromotionError("prospective_challenge_not_frozen","challenge must be frozen before observation")
        if self.start_known_time_ms<0 or self.end_known_time_ms<=self.start_known_time_ms: raise PromotionError("invalid_challenge_window","invalid prospective window")
        if self.required_sample_count<1: raise PromotionError("invalid_required_sample_count","required samples must be positive")
    @property
    def freeze_hash(self)->str: return canonical_sha256(asdict(self))

@dataclass(frozen=True, slots=True)
class PromotionPolicy:
    policy_id: str
    policy_version: str
    alpha: float = 0.05
    minimum_score: float = 0.80
    minimum_effective_sample_size: float = 30.0
    maximum_pbo: float = 0.30
    minimum_deflated_probability: float = 0.95
    maximum_reality_check_p: float = 0.05
    minimum_stress_retention: float = 0.60
    maximum_ece: float = 0.08
    coverage_tolerance: float = 0.03
    mandatory_nulls: tuple[NullKind,...] = (NullKind.MANUAL_BASELINE, NullKind.MATCHED_TIME, NullKind.RANDOM_DIRECTION)
    critical_families: tuple[str,...] = ("integrity","causality","selection","multiplicity","parity","safety")
    allow_manual_override_to_promote: bool = False
    def __post_init__(self)->None:
        _id(self.policy_id,"policy_id"); _semver(self.policy_version,"policy_version")
        for n in ("alpha","minimum_score","maximum_pbo","minimum_deflated_probability","maximum_reality_check_p","minimum_stress_retention","maximum_ece","coverage_tolerance"): _prob(getattr(self,n),n)
        if self.minimum_effective_sample_size<=0: raise PromotionError("invalid_minimum_ess","minimum ESS must be positive")
        if not self.mandatory_nulls: raise PromotionError("empty_mandatory_nulls","at least one mandatory null is required")
    @property
    def policy_hash(self)->str: return canonical_sha256(asdict(self))

@dataclass(frozen=True, slots=True)
class ModelRiskScorecard:
    scorecard_id: str
    component_scores: Mapping[str,float]
    weighted_score: float
    critical_blockers: tuple[str,...]
    high_risks: tuple[str,...]
    residual_risks: tuple[str,...]
    evidence_hash: str
    def __post_init__(self)->None:
        _id(self.scorecard_id,"scorecard_id"); _hash(self.evidence_hash,"evidence_hash"); _prob(self.weighted_score,"weighted_score")
        for n,v in self.component_scores.items(): _id(n,"component_score_name"); _prob(v,f"component_scores.{n}")

@dataclass(frozen=True, slots=True)
class PromotionDecision:
    decision_id: str
    candidate_key: str
    role: DecisionRole
    outcome: GateOutcome
    policy_hash: str
    universe_hash: str
    scorecard_hash: str
    evidence_bundle_hash: str
    blockers: tuple[str,...]
    challenges: tuple[str,...]
    residual_risks: tuple[str,...]
    prospective_freeze_hash: str
    signed: bool
    def __post_init__(self)->None:
        _id(self.decision_id,"decision_id"); _id(self.candidate_key,"candidate_key")
        for n in ("policy_hash","universe_hash","scorecard_hash","evidence_bundle_hash","prospective_freeze_hash"): _hash(getattr(self,n),n)
        if self.outcome is GateOutcome.PROMOTE and (self.blockers or not self.signed): raise PromotionError("invalid_promote_decision","promotion requires no blockers and signed evidence")
        if self.outcome is GateOutcome.REJECT and not self.blockers: raise PromotionError("reject_without_blocker","rejection requires blocker")

@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    bundle_id: str
    bundle_version: str
    candidate_key: str
    universe_hash: str
    policy_hash: str
    artifact_hashes: Mapping[str,str]
    generated_known_time_ms: int
    signer_key_id: str
    signature: str = ""
    def __post_init__(self)->None:
        _id(self.bundle_id,"bundle_id"); _semver(self.bundle_version,"bundle_version"); _id(self.candidate_key,"candidate_key")
        _hash(self.universe_hash,"universe_hash"); _hash(self.policy_hash,"policy_hash"); _id(self.signer_key_id,"signer_key_id")
        if self.generated_known_time_ms<0: raise PromotionError("negative_known_time","generated known time must be non-negative")
        if not self.artifact_hashes: raise PromotionError("empty_evidence_bundle","evidence bundle cannot be empty")
        for n,v in self.artifact_hashes.items(): _id(n,"artifact_name"); _hash(v,f"artifact_hashes.{n}")
        if self.signature and not _SHA.match(self.signature): raise PromotionError("invalid_signature","signature must be SHA-256 hex")
    @property
    def unsigned_payload(self)->Mapping[str,Any]:
        d=asdict(self); d["signature"]=""; return d
    @property
    def bundle_hash(self)->str: return canonical_sha256(asdict(self))
