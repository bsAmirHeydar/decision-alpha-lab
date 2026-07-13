"""Machine-readable UCE-I10 contracts.

The module intentionally contains no training logic. It defines the immutable
surfaces that separate view construction, training, qualification, export, and
runtime consumers. Every behavior-changing field is part of canonical identity.
"""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from .canonical import canonical_sha256, stable_id
from .enums import (
    AdmissionDecision,
    DeepFamily,
    DependencyStatus,
    ExportPath,
    FusionKind,
    QualificationDecision,
    RegimeGateDecision,
    TransferDecision,
)
from .errors import DeepViewError

_SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _require_text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DeepViewError("required_text_missing", f"{name} is required", {"field": name})


def _require_semver(value: str, name: str) -> None:
    _require_text(value, name)
    if not _SEMVER_RE.match(value):
        raise DeepViewError("invalid_semver", f"{name} must be semantic version text", {"value": value})


def _require_finite(value: float, name: str) -> None:
    if not math.isfinite(float(value)):
        raise DeepViewError("non_finite_value", f"{name} must be finite", {"value": repr(value)})


def _validate_hash(value: str, name: str, allow_blank: bool = False) -> None:
    if allow_blank and not value:
        return
    if not _SHA256_RE.match(value):
        raise DeepViewError("invalid_sha256", f"{name} must be a lowercase SHA-256 hex digest", {"value": value})


def _shape_width(shape: tuple[int, ...]) -> int:
    width = 1
    for dimension in shape:
        width *= int(dimension)
    return width


@dataclass(frozen=True, slots=True)
class DeepAlgorithmDescriptor:
    algorithm_id: str
    algorithm_version: str
    family: DeepFamily
    formulation: str
    view_kinds: tuple[str, ...]
    tasks: tuple[str, ...]
    native: bool
    determinism: str
    required_fields: tuple[str, ...]
    output_semantics: tuple[str, ...]
    dependency_profile: str = ""
    export_paths: tuple[ExportPath, ...] = (ExportPath.NATIVE_JSON,)
    default_parameters: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.algorithm_id, "algorithm_id")
        _require_semver(self.algorithm_version, "algorithm_version")
        _require_text(self.formulation, "formulation")
        if not self.view_kinds or not self.tasks or not self.output_semantics:
            raise DeepViewError("empty_algorithm_capability", "algorithm capability lists cannot be empty")
        if self.native and self.dependency_profile:
            raise DeepViewError(
                "native_dependency_profile_forbidden",
                "native algorithms cannot require an optional dependency profile",
                {"algorithm": self.key},
            )
        if not self.export_paths:
            raise DeepViewError("empty_export_paths", "at least one export path must be declared")

    @property
    def key(self) -> str:
        return f"{self.algorithm_id}@{self.algorithm_version}"

    @property
    def descriptor_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class ViewTensorSpec:
    view_id: str
    view_version: str
    view_kind: str
    shape: tuple[int, ...]
    layout: str
    feature_order: tuple[str, ...]
    context_observation_id: str
    known_time_ms: int
    descriptor_hash: str
    payload_hash: str
    mask_required: bool
    runtime_exportable: bool

    def __post_init__(self) -> None:
        _require_text(self.view_id, "view_id")
        _require_semver(self.view_version, "view_version")
        _require_text(self.view_kind, "view_kind")
        _require_text(self.layout, "layout")
        _require_text(self.context_observation_id, "context_observation_id")
        if not self.shape or any(int(value) < 1 for value in self.shape):
            raise DeepViewError("invalid_view_shape", "shape dimensions must be positive")
        if self.known_time_ms < 0:
            raise DeepViewError("negative_known_time", "known_time_ms must be non-negative")
        if self.feature_order and len(set(self.feature_order)) != len(self.feature_order):
            raise DeepViewError("duplicate_feature_name", "feature_order must be unique")
        _validate_hash(self.descriptor_hash, "descriptor_hash", allow_blank=True)
        _validate_hash(self.payload_hash, "payload_hash", allow_blank=True)

    @property
    def width(self) -> int:
        return _shape_width(self.shape)

    @property
    def spec_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class SequenceWindowSpec:
    sequence_id: str
    version: str
    steps: int
    feature_order: tuple[str, ...]
    layout: str = "time_major"
    pad_value: float = 0.0
    require_strict_time: bool = True

    def __post_init__(self) -> None:
        _require_text(self.sequence_id, "sequence_id")
        _require_semver(self.version, "version")
        if self.steps < 1 or not self.feature_order:
            raise DeepViewError("invalid_sequence_window", "steps and feature_order must be non-empty")
        if len(set(self.feature_order)) != len(self.feature_order):
            raise DeepViewError("duplicate_sequence_feature", "sequence feature names must be unique")
        if self.layout not in ("time_major", "feature_major"):
            raise DeepViewError("unsupported_sequence_layout", "layout must be time_major or feature_major")
        _require_finite(self.pad_value, "pad_value")

    @property
    def shape(self) -> tuple[int, int]:
        return self.steps, len(self.feature_order)

    @property
    def spec_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class SequenceArtifact:
    artifact_id: str
    spec_hash: str
    context_observation_id: str
    known_time_ms: int
    timestamps_ms: tuple[int, ...]
    values: tuple[float, ...]
    mask: tuple[int, ...]
    source_hash: str
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.context_observation_id, "context_observation_id")
        _validate_hash(self.spec_hash, "spec_hash")
        _validate_hash(self.source_hash, "source_hash")
        _validate_hash(self.evidence_hash, "evidence_hash")
        if self.known_time_ms < 0:
            raise DeepViewError("negative_known_time", "known_time_ms must be non-negative")
        if any(value not in (0, 1) for value in self.mask):
            raise DeepViewError("invalid_sequence_mask", "sequence mask must be binary")


@dataclass(frozen=True, slots=True)
class DeepViewSample:
    row_id: str
    context_observation_id: str
    known_time_ms: int
    view_specs: Mapping[str, ViewTensorSpec]
    view_values: Mapping[str, tuple[float, ...]]
    view_masks: Mapping[str, tuple[int, ...]]
    target: tuple[float, ...]
    cluster_id: str = ""
    sample_weight: float = 1.0

    def __post_init__(self) -> None:
        _require_text(self.row_id, "row_id")
        _require_text(self.context_observation_id, "context_observation_id")
        _require_finite(self.sample_weight, "sample_weight")
        if self.sample_weight <= 0:
            raise DeepViewError("invalid_sample_weight", "sample_weight must be positive")
        if set(self.view_specs) != set(self.view_values):
            raise DeepViewError("view_key_mismatch", "view_specs and view_values keys differ")
        if not self.target:
            raise DeepViewError("empty_target", "target cannot be empty")
        for value in self.target:
            _require_finite(value, "target")
        for key, spec in self.view_specs.items():
            values = self.view_values[key]
            if len(values) != spec.width:
                raise DeepViewError("view_width_mismatch", "view payload width differs from shape", {"view": key})
            if spec.context_observation_id != self.context_observation_id:
                raise DeepViewError("cross_context_view", "view belongs to a different context", {"view": key})
            if spec.known_time_ms > self.known_time_ms:
                raise DeepViewError("future_view_known_time", "view known-time exceeds sample known-time", {"view": key})
            for value in values:
                _require_finite(value, f"view_values[{key}]")
            mask = self.view_masks.get(key, ())
            if spec.mask_required and len(mask) != spec.width:
                raise DeepViewError("view_mask_width_mismatch", "view mask width differs", {"view": key})
            if mask and any(item not in (0, 1) for item in mask):
                raise DeepViewError("invalid_view_mask", "view mask must be binary", {"view": key})

    @property
    def sample_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class DeepAdmissionEvidence:
    evidence_id: str
    dataset_id: str
    dataset_manifest_hash: str
    effective_sample_size: float
    dependence_cluster_count: int
    event_diversity_count: int
    stable_dimensions: bool
    known_time_audit_passed: bool
    future_perturbation_passed: bool
    classical_gate_passed: bool
    classical_best_metric: float
    augmentation_policy_hash: str
    ablation_plan_hash: str
    decision: AdmissionDecision
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_text(self.evidence_id, "evidence_id")
        _require_text(self.dataset_id, "dataset_id")
        _require_finite(self.effective_sample_size, "effective_sample_size")
        _require_finite(self.classical_best_metric, "classical_best_metric")
        if min(self.dependence_cluster_count, self.event_diversity_count) < 0:
            raise DeepViewError("negative_admission_count", "admission counts cannot be negative")
        if self.decision is AdmissionDecision.REJECT and not self.blockers:
            raise DeepViewError("reject_without_blocker", "rejected admission evidence must name blockers")


@dataclass(frozen=True, slots=True)
class SeedRunObservation:
    seed: int
    status: str
    primary_metric: float
    economic_utility: float
    calibration_error: float
    fit_ms: int
    predict_ms: int
    artifact_hash: str
    error_code: str = ""

    def __post_init__(self) -> None:
        _require_text(self.status, "status")
        for name, value in (
            ("primary_metric", self.primary_metric),
            ("economic_utility", self.economic_utility),
            ("calibration_error", self.calibration_error),
        ):
            _require_finite(value, name)
        if self.fit_ms < 0 or self.predict_ms < 0:
            raise DeepViewError("negative_runtime", "fit and predict durations cannot be negative")


@dataclass(frozen=True, slots=True)
class ViewAblationObservation:
    view_id: str
    full_metric: float
    ablated_metric: float
    incremental_value: float
    economic_incremental_value: float
    passed: bool
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_text(self.view_id, "view_id")
        for name, value in (
            ("full_metric", self.full_metric),
            ("ablated_metric", self.ablated_metric),
            ("incremental_value", self.incremental_value),
            ("economic_incremental_value", self.economic_incremental_value),
        ):
            _require_finite(value, name)


@dataclass(frozen=True, slots=True)
class ExportAssessment:
    path: ExportPath
    available: bool
    parity_max_abs_error: float
    latency_ms: float
    artifact_hash: str
    reason: str
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_finite(self.parity_max_abs_error, "parity_max_abs_error")
        _require_finite(self.latency_ms, "latency_ms")
        if self.parity_max_abs_error < 0 or self.latency_ms < 0:
            raise DeepViewError("negative_export_measure", "export parity and latency cannot be negative")
        if self.available and self.path is ExportPath.NONE:
            raise DeepViewError("available_export_without_path", "available export cannot use path=none")


@dataclass(frozen=True, slots=True)
class DeepQualificationReport:
    report_id: str
    algorithm_key: str
    dataset_manifest_hash: str
    admission_evidence_id: str
    seed_runs: tuple[SeedRunObservation, ...]
    ablations: tuple[ViewAblationObservation, ...]
    export: ExportAssessment
    baseline_metric: float
    mean_metric: float
    metric_std: float
    mean_economic_utility: float
    failed_run_rate: float
    minimum_incremental_uplift: float
    decision: QualificationDecision
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_text(self.report_id, "report_id")
        _require_text(self.algorithm_key, "algorithm_key")
        for name, value in (
            ("baseline_metric", self.baseline_metric),
            ("mean_metric", self.mean_metric),
            ("metric_std", self.metric_std),
            ("mean_economic_utility", self.mean_economic_utility),
            ("failed_run_rate", self.failed_run_rate),
            ("minimum_incremental_uplift", self.minimum_incremental_uplift),
        ):
            _require_finite(value, name)
        if not 0.0 <= self.failed_run_rate <= 1.0:
            raise DeepViewError("invalid_failed_run_rate", "failed_run_rate must be in [0,1]")
        if self.decision is QualificationDecision.REJECTED and not self.blockers:
            raise DeepViewError("qualification_reject_without_blocker", "rejected qualification must name blockers")


@dataclass(frozen=True, slots=True)
class RasterSpec:
    raster_id: str
    version: str
    height: int
    width: int
    channels: tuple[str, ...]
    price_normalization: str
    overlay_policy: str
    augmentation_policy_hash: str

    def __post_init__(self) -> None:
        _require_text(self.raster_id, "raster_id")
        _require_semver(self.version, "version")
        if self.height < 4 or self.width < 1 or not self.channels:
            raise DeepViewError("invalid_raster_dimensions", "raster dimensions/channels are invalid")
        if len(set(self.channels)) != len(self.channels):
            raise DeepViewError("duplicate_raster_channel", "raster channels must be unique")
        allowed_channels = {"wick", "body", "direction", "volume", "close", "range"}
        unknown = sorted(set(self.channels) - allowed_channels)
        if unknown:
            raise DeepViewError("unknown_raster_channel", "raster contains unknown channels", {"channels": unknown})
        if self.price_normalization not in ("window_min_max", "last_close_range"):
            raise DeepViewError("unsupported_price_normalization", "unsupported raster normalization")
        if self.overlay_policy not in ("none", "causal_numeric_only"):
            raise DeepViewError("unsupported_overlay_policy", "unsupported overlay policy")

    @property
    def spec_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class RasterArtifact:
    artifact_id: str
    spec_hash: str
    context_observation_id: str
    known_time_ms: int
    shape: tuple[int, int, int]
    values: tuple[float, ...]
    source_hash: str
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.context_observation_id, "context_observation_id")
        if len(self.shape) != 3 or any(int(value) < 1 for value in self.shape):
            raise DeepViewError("invalid_raster_shape", "raster artifact shape must be CxHxW")
        if len(self.values) != _shape_width(self.shape):
            raise DeepViewError("raster_payload_width_mismatch", "raster payload width differs from shape")
        if self.known_time_ms < 0:
            raise DeepViewError("negative_known_time", "known_time_ms must be non-negative")


@dataclass(frozen=True, slots=True)
class PixelAuditReport:
    report_id: str
    artifact_a_hash: str
    artifact_b_hash: str
    max_abs_difference: float
    changed_pixel_count: int
    prefix_invariant: bool
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class GraphSpec:
    graph_id: str
    version: str
    node_feature_order: tuple[str, ...]
    directed: bool
    message_passing_rounds: int
    topology_version: str

    def __post_init__(self) -> None:
        _require_text(self.graph_id, "graph_id")
        _require_semver(self.version, "version")
        _require_text(self.topology_version, "topology_version")
        if not self.node_feature_order:
            raise DeepViewError("empty_graph_features", "node_feature_order cannot be empty")
        if len(set(self.node_feature_order)) != len(self.node_feature_order):
            raise DeepViewError("duplicate_graph_feature", "graph feature names must be unique")
        if self.message_passing_rounds < 0:
            raise DeepViewError("negative_message_rounds", "message-passing rounds cannot be negative")

    @property
    def spec_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class GraphArtifact:
    artifact_id: str
    spec_hash: str
    context_observation_id: str
    known_time_ms: int
    node_ids: tuple[str, ...]
    node_times_ms: tuple[int, ...]
    node_features: tuple[tuple[float, ...], ...]
    edges: tuple[tuple[int, int], ...]
    topology_hash: str
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.context_observation_id, "context_observation_id")
        count = len(self.node_ids)
        if count < 1 or len(self.node_times_ms) != count or len(self.node_features) != count:
            raise DeepViewError("graph_node_width_mismatch", "graph node arrays must have equal non-zero length")
        if len(set(self.node_ids)) != count:
            raise DeepViewError("duplicate_graph_node_id", "graph node IDs must be unique")
        if any(time > self.known_time_ms for time in self.node_times_ms):
            raise DeepViewError("future_graph_node", "graph contains a future node")
        for source, target in self.edges:
            if source < 0 or target < 0 or source >= count or target >= count:
                raise DeepViewError("graph_edge_out_of_range", "graph edge endpoint is out of range")


@dataclass(frozen=True, slots=True)
class RegimeNoveltyPrediction:
    prediction_id: str
    row_id: str
    regime_id: str
    regime_probability: float
    novelty_score: float
    change_score: float
    support_count: int
    decision: RegimeGateDecision
    expert_key: str
    reason: str
    evidence_hash: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.regime_probability <= 1.0:
            raise DeepViewError("invalid_regime_probability", "regime probability must be in [0,1]")
        if self.support_count < 0:
            raise DeepViewError("negative_regime_support", "support_count cannot be negative")


@dataclass(frozen=True, slots=True)
class FusionPrediction:
    prediction_id: str
    row_id: str
    fusion_kind: FusionKind
    available_views: tuple[str, ...]
    missing_views: tuple[str, ...]
    view_weights: Mapping[str, float]
    value: float
    uncertainty: float
    abstained: bool
    reason: str
    evidence_hash: str

    def __post_init__(self) -> None:
        _require_finite(self.value, "value")
        _require_finite(self.uncertainty, "uncertainty")
        if self.uncertainty < 0:
            raise DeepViewError("negative_fusion_uncertainty", "fusion uncertainty cannot be negative")
        if set(self.available_views) & set(self.missing_views):
            raise DeepViewError("fusion_view_status_overlap", "a fusion view cannot be available and missing")
        if self.view_weights:
            total = sum(float(value) for value in self.view_weights.values())
            if abs(total - 1.0) > 1e-9:
                raise DeepViewError("fusion_weights_not_normalized", "fusion weights must sum to one", {"sum": total})


@dataclass(frozen=True, slots=True)
class DistillationReport:
    report_id: str
    teacher_key: str
    student_key: str
    row_count: int
    teacher_metric: float
    student_metric: float
    fidelity_mae: float
    compression_ratio: float
    accepted: bool
    limitations: tuple[str, ...]
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class QuantizationReport:
    report_id: str
    bits: int
    scale: float
    zero_point: int
    max_abs_error: float
    mean_abs_error: float
    accepted: bool
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class DependencyProbe:
    profile: str
    module: str
    status: DependencyStatus
    detected_version: str
    minimum_version: str
    reason: str
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class TransferBoundary:
    boundary_id: str
    source_dataset_manifest_hash: str
    target_dataset_manifest_hash: str
    source_row_ids_hash: str
    target_train_row_ids_hash: str
    target_final_test_row_ids_hash: str
    representation_frozen: bool
    decision: TransferDecision
    blockers: tuple[str, ...]
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class DeepRegistrySnapshot:
    snapshot_id: str
    descriptors: tuple[DeepAlgorithmDescriptor, ...]
    frozen: bool
    evidence_hash: str


def make_evidence_id(prefix: str, material: Any) -> str:
    return stable_id(prefix, material)
