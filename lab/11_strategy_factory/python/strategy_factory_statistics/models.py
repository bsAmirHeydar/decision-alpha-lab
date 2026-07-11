from __future__ import annotations
from dataclasses import dataclass, asdict
import math
from .enums import NullMethod, ReportStatus, IntervalKind
from .hashing import stable_id

@dataclass(frozen=True, slots=True)
class StatisticalSample:
    sample_id: str
    outcome_id: str
    candidate_id: str
    event_id: str
    cluster_id: str
    strategy_id: str
    symbol: str
    direction: str
    session_id: str
    year: int
    month: int
    weekday: int
    stratum_key: str
    filled: bool
    ambiguous: bool
    net_r: float
    mfe_r: float
    mae_r: float
    holding_seconds: float
    weight: float = 1.0
    known_time_utc_msc: int = 0

    def validate(self) -> None:
        ids = (self.sample_id, self.outcome_id, self.candidate_id, self.event_id,
               self.cluster_id, self.strategy_id, self.symbol, self.stratum_key)
        if any(not x for x in ids):
            raise ValueError("missing statistical sample identity")
        values = (self.net_r, self.mfe_r, self.mae_r, self.holding_seconds, self.weight)
        if any(not math.isfinite(v) for v in values):
            raise ValueError("non-finite statistical sample")
        if self.mfe_r < 0 or self.mae_r < 0 or self.holding_seconds < 0 or self.weight <= 0:
            raise ValueError("invalid statistical sample bounds")
        if not 1 <= self.month <= 12 or not 0 <= self.weekday <= 6:
            raise ValueError("invalid calendar fields")

@dataclass(frozen=True, slots=True)
class StatisticSummary:
    group_key: str
    sample_count: int
    filled_count: int
    win_count: int
    loss_count: int
    flat_count: int
    unique_event_count: int
    unique_cluster_count: int
    fill_rate: float
    win_rate: float
    mean_net_r: float
    median_net_r: float
    standard_deviation_r: float
    standard_error_r: float
    profit_factor: float
    total_net_r: float
    maximum_drawdown_r: float
    average_mfe_r: float
    average_mae_r: float
    average_holding_seconds: float
    q05_net_r: float
    q25_net_r: float
    q75_net_r: float
    q95_net_r: float
    best_trade_r: float
    worst_trade_r: float
    best_trade_share: float
    status: ReportStatus = ReportStatus.VALID
    summary_hash: str = ""

    def canonical(self) -> str:
        vals = [self.group_key, self.sample_count, self.filled_count,
                self.unique_event_count, self.unique_cluster_count,
                self.fill_rate, self.win_rate, self.mean_net_r,
                self.standard_deviation_r, self.profit_factor,
                self.total_net_r, self.maximum_drawdown_r,
                self.best_trade_share, int(self.status)]
        return "alpha_lab.strategy_factory/statistic_summary@1.0.0|" + "|".join(map(str, vals))

    def with_hash(self) -> "StatisticSummary":
        return type(self)(**{**asdict(self), "status": self.status,
                             "summary_hash": stable_id("stat", self.canonical())})

@dataclass(frozen=True, slots=True)
class ConfidenceInterval:
    metric_id: str
    group_key: str
    kind: IntervalKind
    confidence_level: float
    estimate: float
    lower: float
    upper: float
    standard_error: float
    effective_sample_count: int
    seed: int = 0
    interval_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, ["alpha_lab.strategy_factory/confidence_interval@1.0.0",
            self.metric_id, self.group_key, int(self.kind), self.confidence_level,
            self.estimate, self.lower, self.upper, self.standard_error,
            self.effective_sample_count, self.seed]))

    def with_hash(self) -> "ConfidenceInterval":
        return type(self)(**{**asdict(self), "kind": self.kind,
                             "interval_hash": stable_id("cint", self.canonical())})

@dataclass(frozen=True, slots=True)
class MatchedNullSpec:
    null_id: str
    null_version: str
    method: NullMethod
    seed: int
    minimum_pool_size: int
    maximum_reuse: int
    require_different_cluster: bool
    required_stratum_fields: tuple[str, ...]
    null_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, ["alpha_lab.strategy_factory/matched_null_spec@1.0.0",
            self.null_id, self.null_version, int(self.method), self.seed,
            self.minimum_pool_size, self.maximum_reuse,
            self.require_different_cluster, ",".join(self.required_stratum_fields)]))

    def with_hash(self) -> "MatchedNullSpec":
        return type(self)(**{**asdict(self), "method": self.method,
                             "required_stratum_fields": self.required_stratum_fields,
                             "null_hash": stable_id("null", self.canonical())})

@dataclass(frozen=True, slots=True)
class NullAssignment:
    assignment_id: str
    null_hash: str
    observed_sample_id: str
    control_sample_id: str
    stratum_key: str
    observed_cluster_id: str
    control_cluster_id: str
    reuse_ordinal: int

@dataclass(frozen=True, slots=True)
class NullComparison:
    null_hash: str
    group_key: str
    matched_count: int
    observed_mean_r: float
    control_mean_r: float
    uplift_r: float
    paired_standard_error: float
    z_score: float
    match_rate: float
    status: ReportStatus
    comparison_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, ["alpha_lab.strategy_factory/null_comparison@1.0.0",
            self.null_hash, self.group_key, self.matched_count, self.observed_mean_r,
            self.control_mean_r, self.uplift_r, self.paired_standard_error,
            self.z_score, self.match_rate, int(self.status)]))

    def with_hash(self) -> "NullComparison":
        return type(self)(**{**asdict(self), "status": self.status,
                             "comparison_hash": stable_id("ncmp", self.canonical())})

@dataclass(frozen=True, slots=True)
class StatisticalReportManifest:
    report_id: str
    report_program_id: str
    report_version: str
    source_run_id: str
    source_manifest_hash: str
    source_artifact_hash: str
    strategy_id: str
    strategy_version: str
    candidate_matrix_hash: str
    simulation_policy_hash: str
    cost_registry_hash: str
    group_schema_hash: str
    metric_registry_hash: str
    null_registry_hash: str
    random_seed: int
    generated_at_utc_msc: int
    git_commit: str
    manifest_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, ["alpha_lab.strategy_factory/statistical_report_manifest@1.0.0",
            self.report_id, self.report_program_id, self.report_version,
            self.source_run_id, self.source_manifest_hash, self.source_artifact_hash,
            self.strategy_id, self.strategy_version, self.candidate_matrix_hash,
            self.simulation_policy_hash, self.cost_registry_hash, self.group_schema_hash,
            self.metric_registry_hash, self.null_registry_hash, self.random_seed,
            self.generated_at_utc_msc, self.git_commit]))

    def with_hash(self) -> "StatisticalReportManifest":
        return type(self)(**{**asdict(self), "manifest_hash": stable_id("srep", self.canonical())})

    def validate(self) -> None:
        required = [self.report_id, self.report_program_id, self.report_version,
                    self.source_run_id, self.source_manifest_hash, self.source_artifact_hash,
                    self.strategy_id, self.strategy_version, self.candidate_matrix_hash,
                    self.simulation_policy_hash, self.cost_registry_hash,
                    self.group_schema_hash, self.metric_registry_hash,
                    self.null_registry_hash, self.git_commit]
        if any(not x for x in required):
            raise ValueError("missing report lineage")
        if self.generated_at_utc_msc < 0:
            raise ValueError("invalid report timestamp")
        if self.manifest_hash and self.manifest_hash != stable_id("srep", self.canonical()):
            raise ValueError("report manifest hash mismatch")

@dataclass(frozen=True, slots=True)
class ReportArtifactIndex:
    report_id: str
    manifest_hash: str
    artifacts: tuple[tuple[str, str, str], ...]
    index_hash: str = ""

    def canonical(self) -> str:
        payload = ";".join("|".join(x) for x in self.artifacts)
        return f"alpha_lab.strategy_factory/report_artifact_index@1.0.0|{self.report_id}|{self.manifest_hash}|{payload}"

    def with_hash(self) -> "ReportArtifactIndex":
        return type(self)(self.report_id, self.manifest_hash, self.artifacts,
                          stable_id("ridx", self.canonical()))
