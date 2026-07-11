from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable
import math
from .enums import SplitMethod, FoldRole, GateStatus, PromotionStatus, StressKind, LeakageSeverity
from .hashing import stable_id

SCHEMA_PREFIX = "alpha_lab.strategy_factory"

@dataclass(frozen=True, slots=True)
class TimeRange:
    start_utc_msc: int
    end_utc_msc: int

    def validate(self) -> None:
        if self.start_utc_msc < 0 or self.end_utc_msc <= self.start_utc_msc:
            raise ValueError("invalid half-open time range")

    def contains(self, timestamp_utc_msc: int) -> bool:
        return self.start_utc_msc <= timestamp_utc_msc < self.end_utc_msc

    @property
    def span_msc(self) -> int:
        return self.end_utc_msc - self.start_utc_msc

@dataclass(frozen=True, slots=True)
class ValidationPlan:
    plan_id: str
    plan_version: str
    method: SplitMethod
    source_run_id: str
    source_manifest_hash: str
    source_artifact_hash: str
    strategy_id: str
    search_space_hash: str
    start_utc_msc: int
    end_utc_msc: int
    train_span_msc: int
    validation_span_msc: int
    test_span_msc: int
    step_span_msc: int
    purge_span_msc: int
    embargo_span_msc: int
    minimum_train_samples: int
    minimum_validation_samples: int
    minimum_test_samples: int
    maximum_folds: int = 128
    random_seed: int = 120011
    plan_hash: str = ""

    def canonical(self) -> str:
        values = [f"{SCHEMA_PREFIX}/validation_plan@1.0.0", self.plan_id,
                  self.plan_version, int(self.method), self.source_run_id,
                  self.source_manifest_hash, self.source_artifact_hash,
                  self.strategy_id, self.search_space_hash, self.start_utc_msc,
                  self.end_utc_msc, self.train_span_msc,
                  self.validation_span_msc, self.test_span_msc,
                  self.step_span_msc, self.purge_span_msc,
                  self.embargo_span_msc, self.minimum_train_samples,
                  self.minimum_validation_samples, self.minimum_test_samples,
                  self.maximum_folds, self.random_seed]
        return "|".join(map(str, values))

    def with_hash(self) -> "ValidationPlan":
        return type(self)(**{**asdict(self), "method": self.method,
                             "plan_hash": stable_id("vplan", self.canonical())})

    def validate(self) -> None:
        required = (self.plan_id, self.plan_version, self.source_run_id,
                    self.source_manifest_hash, self.source_artifact_hash,
                    self.strategy_id, self.search_space_hash)
        if any(not x for x in required):
            raise ValueError("missing validation-plan lineage")
        if self.end_utc_msc <= self.start_utc_msc:
            raise ValueError("invalid validation-plan horizon")
        if min(self.train_span_msc, self.validation_span_msc,
               self.test_span_msc, self.step_span_msc) <= 0:
            raise ValueError("non-positive fold span")
        if min(self.purge_span_msc, self.embargo_span_msc) < 0:
            raise ValueError("negative purge or embargo")
        if min(self.minimum_train_samples, self.minimum_validation_samples,
               self.minimum_test_samples) < 1:
            raise ValueError("minimum sample count must be positive")
        if not 1 <= self.maximum_folds <= 4096:
            raise ValueError("maximum_folds outside supported bound")
        expected = stable_id("vplan", self.canonical())
        if self.plan_hash and self.plan_hash != expected:
            raise ValueError("validation-plan hash mismatch")

@dataclass(frozen=True, slots=True)
class ValidationFold:
    fold_id: str
    ordinal: int
    train: TimeRange
    validation: TimeRange
    test: TimeRange
    purge_before_validation: TimeRange | None
    embargo_before_test: TimeRange | None
    plan_hash: str
    fold_hash: str = ""

    def canonical(self) -> str:
        parts = [f"{SCHEMA_PREFIX}/validation_fold@1.0.0", self.fold_id,
                 self.ordinal, self.plan_hash, self.train.start_utc_msc,
                 self.train.end_utc_msc, self.validation.start_utc_msc,
                 self.validation.end_utc_msc, self.test.start_utc_msc,
                 self.test.end_utc_msc]
        for gap in (self.purge_before_validation, self.embargo_before_test):
            parts.extend([gap.start_utc_msc, gap.end_utc_msc] if gap else [0, 0])
        return "|".join(map(str, parts))

    def with_hash(self) -> "ValidationFold":
        return type(self)(**{**asdict(self), "train": self.train,
                             "validation": self.validation, "test": self.test,
                             "purge_before_validation": self.purge_before_validation,
                             "embargo_before_test": self.embargo_before_test,
                             "fold_hash": stable_id("vfold", self.canonical())})

    def validate(self) -> None:
        self.train.validate(); self.validation.validate(); self.test.validate()
        if not self.fold_id or not self.plan_hash or self.ordinal < 0:
            raise ValueError("invalid fold identity")
        if self.train.end_utc_msc > self.validation.start_utc_msc:
            raise ValueError("train overlaps validation")
        if self.validation.end_utc_msc > self.test.start_utc_msc:
            raise ValueError("validation overlaps test")
        expected = stable_id("vfold", self.canonical())
        if self.fold_hash and self.fold_hash != expected:
            raise ValueError("validation-fold hash mismatch")

@dataclass(frozen=True, slots=True)
class FoldObservation:
    observation_id: str
    trial_id: str
    parameter_hash: str
    fold_id: str
    role: FoldRole
    event_id: str
    cluster_id: str
    outcome_id: str
    known_time_utc_msc: int
    resolved_time_utc_msc: int
    net_r: float
    gross_r: float
    cost_r: float
    ambiguous: bool = False
    observation_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/fold_observation@1.0.0",
            self.observation_id, self.trial_id, self.parameter_hash, self.fold_id,
            int(self.role), self.event_id, self.cluster_id, self.outcome_id,
            self.known_time_utc_msc, self.resolved_time_utc_msc,
            format(self.net_r, ".17g"), format(self.gross_r, ".17g"),
            format(self.cost_r, ".17g"), self.ambiguous]))

    def with_hash(self) -> "FoldObservation":
        return type(self)(**{**asdict(self), "role": self.role,
                             "observation_hash": stable_id("fobs", self.canonical())})

    def validate(self) -> None:
        required = (self.observation_id, self.trial_id, self.parameter_hash,
                    self.fold_id, self.event_id, self.cluster_id, self.outcome_id)
        if any(not x for x in required):
            raise ValueError("missing fold-observation identity")
        if self.known_time_utc_msc < 0 or self.resolved_time_utc_msc < self.known_time_utc_msc:
            raise ValueError("invalid causal timestamps")
        if any(not math.isfinite(x) for x in (self.net_r, self.gross_r, self.cost_r)):
            raise ValueError("non-finite fold observation")
        expected = stable_id("fobs", self.canonical())
        if self.observation_hash and self.observation_hash != expected:
            raise ValueError("fold-observation hash mismatch")

@dataclass(frozen=True, slots=True)
class TrialRecord:
    trial_id: str
    parameter_hash: str
    parameter_vector: tuple[float, ...]
    fold_metrics: tuple[tuple[str, float, float, float], ...]
    discovery_ordinal: int
    trial_hash: str = ""

    def canonical(self) -> str:
        vector = ",".join(format(x, ".17g") for x in self.parameter_vector)
        folds = ";".join("|".join([fid, format(a, ".17g"),
                                     format(b, ".17g"), format(c, ".17g")])
                         for fid, a, b, c in self.fold_metrics)
        return f"{SCHEMA_PREFIX}/trial_record@1.0.0|{self.trial_id}|{self.parameter_hash}|{vector}|{folds}|{self.discovery_ordinal}"

    def with_hash(self) -> "TrialRecord":
        return type(self)(self.trial_id, self.parameter_hash,
                          self.parameter_vector, self.fold_metrics,
                          self.discovery_ordinal,
                          stable_id("trial", self.canonical()))

@dataclass(frozen=True, slots=True)
class ParameterNeighbor:
    left_trial_id: str
    right_trial_id: str
    normalized_distance: float
    neighbor_hash: str = ""

    def canonical(self) -> str:
        a, b = sorted((self.left_trial_id, self.right_trial_id))
        return f"{SCHEMA_PREFIX}/parameter_neighbor@1.0.0|{a}|{b}|{format(self.normalized_distance,'.17g')}"

    def with_hash(self) -> "ParameterNeighbor":
        return type(self)(self.left_trial_id, self.right_trial_id,
                          self.normalized_distance,
                          stable_id("nbr", self.canonical()))

@dataclass(frozen=True, slots=True)
class StressScenario:
    scenario_id: str
    scenario_version: str
    kind: StressKind
    additive_penalty_r: float = 0.0
    drop_fraction: float = 0.0
    remove_best_count: int = 0
    excluded_cluster_id: str = ""
    seed: int = 0
    scenario_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/stress_scenario@1.0.0",
            self.scenario_id, self.scenario_version, int(self.kind),
            format(self.additive_penalty_r, ".17g"),
            format(self.drop_fraction, ".17g"), self.remove_best_count,
            self.excluded_cluster_id, self.seed]))

    def with_hash(self) -> "StressScenario":
        return type(self)(**{**asdict(self), "kind": self.kind,
                             "scenario_hash": stable_id("stress", self.canonical())})

    def validate(self) -> None:
        if not self.scenario_id or not self.scenario_version:
            raise ValueError("missing stress scenario identity")
        if not 0.0 <= self.drop_fraction < 1.0:
            raise ValueError("drop_fraction outside [0,1)")
        if self.remove_best_count < 0:
            raise ValueError("negative remove_best_count")
        if not math.isfinite(self.additive_penalty_r):
            raise ValueError("non-finite stress penalty")

@dataclass(frozen=True, slots=True)
class GateResult:
    gate_id: str
    status: GateStatus
    observed_value: float
    threshold_value: float
    comparison: str
    reason_code: str
    evidence_hash: str

@dataclass(frozen=True, slots=True)
class LeakageFinding:
    finding_id: str
    severity: LeakageSeverity
    code: str
    fold_id: str
    trial_id: str
    event_id: str
    detail: str

@dataclass(frozen=True, slots=True)
class MultipleTestingResult:
    method: str
    hypothesis_ids: tuple[str, ...]
    raw_p_values: tuple[float, ...]
    adjusted_p_values: tuple[float, ...]
    rejected: tuple[bool, ...]
    alpha: float
    result_hash: str

@dataclass(frozen=True, slots=True)
class DeflatedPerformanceResult:
    trial_id: str
    observed_sharpe: float
    expected_max_sharpe: float
    deflated_probability: float
    number_of_trials: int
    sample_count: int
    skewness: float
    kurtosis: float
    result_hash: str

@dataclass(frozen=True, slots=True)
class PBOResult:
    probability_of_backtest_overfitting: float
    median_logit: float
    split_count: int
    selected_trial_counts: tuple[tuple[str, int], ...]
    result_hash: str

@dataclass(frozen=True, slots=True)
class RealityCheckResult:
    winner_trial_id: str
    observed_max_statistic: float
    bootstrap_p_value: float
    bootstrap_iterations: int
    seed: int
    result_hash: str

@dataclass(frozen=True, slots=True)
class SurfaceStabilityResult:
    winner_trial_id: str
    neighbor_count: int
    positive_neighbor_share: float
    median_relative_degradation: float
    normalized_roughness: float
    support_score: float
    result_hash: str

@dataclass(frozen=True, slots=True)
class StressResult:
    scenario_id: str
    trial_id: str
    sample_count: int
    mean_net_r: float
    total_net_r: float
    worst_net_r: float
    retained_fraction: float
    result_hash: str

@dataclass(frozen=True, slots=True)
class PromotionDecision:
    decision_id: str
    plan_hash: str
    selected_trial_id: str
    status: PromotionStatus
    gate_results: tuple[GateResult, ...]
    rejection_reasons: tuple[str, ...]
    evidence_artifact_hashes: tuple[str, ...]
    decision_hash: str = ""

    def canonical(self) -> str:
        gates = ";".join(f"{g.gate_id}|{int(g.status)}|{g.reason_code}|{g.evidence_hash}"
                         for g in self.gate_results)
        return "|".join([f"{SCHEMA_PREFIX}/promotion_decision@1.0.0",
            self.decision_id, self.plan_hash, self.selected_trial_id,
            str(int(self.status)), gates, ",".join(self.rejection_reasons),
            ",".join(self.evidence_artifact_hashes)])

    def with_hash(self) -> "PromotionDecision":
        return type(self)(**{**asdict(self), "status": self.status,
                             "gate_results": self.gate_results,
                             "rejection_reasons": self.rejection_reasons,
                             "evidence_artifact_hashes": self.evidence_artifact_hashes,
                             "decision_hash": stable_id("prom", self.canonical())})

@dataclass(frozen=True, slots=True)
class AntiOverfitReportManifest:
    report_id: str
    report_version: str
    plan_hash: str
    source_run_id: str
    source_manifest_hash: str
    trial_ledger_hash: str
    statistical_report_hash: str
    split_registry_hash: str
    stress_registry_hash: str
    gate_registry_hash: str
    random_seed: int
    generated_at_utc_msc: int
    git_commit: str
    manifest_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/anti_overfit_report_manifest@1.0.0",
            self.report_id, self.report_version, self.plan_hash,
            self.source_run_id, self.source_manifest_hash, self.trial_ledger_hash,
            self.statistical_report_hash, self.split_registry_hash,
            self.stress_registry_hash, self.gate_registry_hash,
            self.random_seed, self.generated_at_utc_msc, self.git_commit]))

    def with_hash(self) -> "AntiOverfitReportManifest":
        return type(self)(**{**asdict(self),
                             "manifest_hash": stable_id("aofrep", self.canonical())})
