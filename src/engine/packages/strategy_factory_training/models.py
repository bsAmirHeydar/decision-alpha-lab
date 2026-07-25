from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable
import math
from .enums import *
from .hashing import stable_id, sha256_lines, cfloat, cbool

SCHEMA_PREFIX = "alpha_lab.strategy_factory"

def _required(*values: str) -> None:
    if any(not value for value in values):
        raise ValueError("missing required lineage or identity")

@dataclass(frozen=True, slots=True)
class FeatureColumn:
    feature_id: str
    feature_version: str
    ordinal: int
    value_type: str = "float64"
    required: bool = True
    source_schema: str = "alpha_lab.strategy_factory/feature_value@1.0.0"
    description: str = ""
    column_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/dataset_feature_column@1.0.0", self.feature_id,
            self.feature_version, self.ordinal, self.value_type, cbool(self.required), self.source_schema,
            self.description]))

    def with_hash(self) -> "FeatureColumn":
        return type(self)(**{**asdict(self), "column_hash": stable_id("fcol", self.canonical())})

    def validate(self) -> None:
        _required(self.feature_id, self.feature_version, self.value_type, self.source_schema)
        if self.ordinal < 0 or self.ordinal >= 4096:
            raise ValueError("feature ordinal outside supported bound")
        expected = stable_id("fcol", self.canonical())
        if self.column_hash and self.column_hash != expected:
            raise ValueError("feature-column hash mismatch")

@dataclass(frozen=True, slots=True)
class LabelContract:
    contract_id: str
    contract_version: str
    kind: LabelKind
    positive_threshold_r: float = 0.0
    regression_floor_r: float = -10.0
    regression_cap_r: float = 10.0
    ambiguous_policy: AmbiguousLabelPolicy = AmbiguousLabelPolicy.EXCLUDE
    require_filled: bool = True
    require_terminal: bool = True
    label_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/label_contract@1.0.0", self.contract_id,
            self.contract_version, int(self.kind), cfloat(self.positive_threshold_r),
            cfloat(self.regression_floor_r), cfloat(self.regression_cap_r),
            int(self.ambiguous_policy), cbool(self.require_filled), cbool(self.require_terminal)]))

    def with_hash(self) -> "LabelContract":
        return type(self)(**{**asdict(self), "kind": self.kind, "ambiguous_policy": self.ambiguous_policy,
            "label_hash": stable_id("lblc", self.canonical())})

    def validate(self) -> None:
        _required(self.contract_id, self.contract_version)
        if self.regression_floor_r >= self.regression_cap_r:
            raise ValueError("invalid regression clipping bounds")
        expected = stable_id("lblc", self.canonical())
        if self.label_hash and self.label_hash != expected:
            raise ValueError("label-contract hash mismatch")

@dataclass(frozen=True, slots=True)
class DatasetRow:
    dataset_id: str
    fold_id: str
    role: DatasetRole
    event_id: str
    cluster_id: str
    candidate_id: str
    outcome_id: str
    feature_snapshot_id: str
    known_time_utc_msc: int
    decision_time_utc_msc: int
    resolved_time_utc_msc: int
    feature_values: tuple[float, ...]
    feature_missing: tuple[bool, ...]
    label_value: float | None
    label_available: bool
    ambiguous: bool
    source_manifest_hash: str
    source_artifact_hash: str
    row_id: str = ""
    row_hash: str = ""

    def canonical_identity(self) -> str:
        return "|".join(map(str, [self.dataset_id, self.fold_id, int(self.role), self.event_id,
            self.cluster_id, self.candidate_id, self.outcome_id, self.feature_snapshot_id,
            self.known_time_utc_msc, self.decision_time_utc_msc]))

    def canonical(self) -> str:
        values = ",".join("NA" if m else cfloat(v) for v, m in zip(self.feature_values, self.feature_missing))
        label = "NA" if self.label_value is None else cfloat(self.label_value)
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/dataset_row@1.0.0", self.row_id,
            self.canonical_identity(), self.resolved_time_utc_msc, values, label,
            cbool(self.label_available), cbool(self.ambiguous), self.source_manifest_hash,
            self.source_artifact_hash]))

    def with_hashes(self) -> "DatasetRow":
        row_id = self.row_id or stable_id("drow", self.canonical_identity())
        candidate = type(self)(**{**asdict(self), "role": self.role, "feature_values": self.feature_values,
            "feature_missing": self.feature_missing, "row_id": row_id, "row_hash": ""})
        return type(self)(**{**asdict(candidate), "role": candidate.role,
            "feature_values": candidate.feature_values, "feature_missing": candidate.feature_missing,
            "row_hash": stable_id("drowh", candidate.canonical())})

    def validate(self, feature_count: int) -> None:
        _required(self.dataset_id, self.fold_id, self.event_id, self.cluster_id, self.candidate_id,
                  self.outcome_id, self.feature_snapshot_id, self.source_manifest_hash, self.source_artifact_hash)
        if self.known_time_utc_msc < 0 or self.decision_time_utc_msc < self.known_time_utc_msc:
            raise ValueError("feature or decision time violates causality")
        if self.resolved_time_utc_msc < self.decision_time_utc_msc:
            raise ValueError("label resolves before the decision")
        if len(self.feature_values) != feature_count or len(self.feature_missing) != feature_count:
            raise ValueError("feature vector width mismatch")
        for value, missing in zip(self.feature_values, self.feature_missing):
            if not missing and not math.isfinite(value):
                raise ValueError("non-finite observed feature")
        if self.label_available != (self.label_value is not None):
            raise ValueError("label availability mismatch")
        if self.label_value is not None and not math.isfinite(self.label_value):
            raise ValueError("non-finite label")
        if self.role in (DatasetRole.PURGED, DatasetRole.EMBARGO) and self.label_available:
            raise ValueError("purged or embargo rows cannot carry trainable labels")
        expected_id = stable_id("drow", self.canonical_identity())
        if self.row_id and self.row_id != expected_id:
            raise ValueError("dataset-row identity mismatch")
        if self.row_hash:
            unhashed = type(self)(**{**asdict(self), "role": self.role, "feature_values": self.feature_values,
                "feature_missing": self.feature_missing, "row_hash": ""})
            if self.row_hash != stable_id("drowh", unhashed.canonical()):
                raise ValueError("dataset-row hash mismatch")

@dataclass(frozen=True, slots=True)
class DatasetManifest:
    dataset_id: str
    dataset_version: str
    strategy_id: str
    source_run_id: str
    source_manifest_hash: str
    source_artifact_hash: str
    validation_plan_hash: str
    feature_schema_hash: str
    label_contract_hash: str
    row_count: int
    train_count: int
    validation_count: int
    test_count: int
    excluded_count: int
    rowset_hash: str
    created_at_utc_msc: int
    code_revision: str
    dataset_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/dataset_manifest@1.0.0", self.dataset_id,
            self.dataset_version, self.strategy_id, self.source_run_id, self.source_manifest_hash,
            self.source_artifact_hash, self.validation_plan_hash, self.feature_schema_hash,
            self.label_contract_hash, self.row_count, self.train_count, self.validation_count,
            self.test_count, self.excluded_count, self.rowset_hash, self.created_at_utc_msc,
            self.code_revision]))

    def with_hash(self) -> "DatasetManifest":
        return type(self)(**{**asdict(self), "dataset_hash": stable_id("dset", self.canonical())})

    def validate(self) -> None:
        _required(self.dataset_id, self.dataset_version, self.strategy_id, self.source_run_id,
                  self.source_manifest_hash, self.source_artifact_hash, self.validation_plan_hash,
                  self.feature_schema_hash, self.label_contract_hash, self.rowset_hash, self.code_revision)
        counts = (self.row_count, self.train_count, self.validation_count, self.test_count, self.excluded_count)
        if any(v < 0 for v in counts):
            raise ValueError("negative dataset count")
        if self.train_count + self.validation_count + self.test_count + self.excluded_count != self.row_count:
            raise ValueError("dataset role counts do not reconcile")
        expected = stable_id("dset", self.canonical())
        if self.dataset_hash and self.dataset_hash != expected:
            raise ValueError("dataset-manifest hash mismatch")

@dataclass(frozen=True, slots=True)
class TransformSpec:
    missing_policy: MissingValuePolicy = MissingValuePolicy.TRAIN_MEDIAN
    scale_policy: ScalePolicy = ScalePolicy.STANDARDIZE
    constant_value: float = 0.0
    minimum_scale: float = 1e-12

    def canonical(self) -> str:
        return "|".join(map(str, [int(self.missing_policy), int(self.scale_policy),
            cfloat(self.constant_value), cfloat(self.minimum_scale)]))

    @property
    def spec_hash(self) -> str:
        return stable_id("tspec", self.canonical())

@dataclass(frozen=True, slots=True)
class TransformState:
    feature_schema_hash: str
    spec_hash: str
    fitted_role: DatasetRole
    fitted_row_count: int
    impute_values: tuple[float, ...]
    means: tuple[float, ...]
    scales: tuple[float, ...]
    fitted_rowset_hash: str
    transform_hash: str = ""

    def canonical(self) -> str:
        vectors = [self.impute_values, self.means, self.scales]
        encoded = [",".join(cfloat(v) for v in vector) for vector in vectors]
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/transform_state@1.0.0",
            self.feature_schema_hash, self.spec_hash, int(self.fitted_role), self.fitted_row_count,
            *encoded, self.fitted_rowset_hash]))

    def with_hash(self) -> "TransformState":
        return type(self)(**{**asdict(self), "fitted_role": self.fitted_role,
            "impute_values": self.impute_values, "means": self.means, "scales": self.scales,
            "transform_hash": stable_id("xform", self.canonical())})

    def validate(self) -> None:
        _required(self.feature_schema_hash, self.spec_hash, self.fitted_rowset_hash)
        if self.fitted_role != DatasetRole.TRAIN or self.fitted_row_count < 1:
            raise ValueError("transform state was not fitted exclusively on training rows")
        if not (len(self.impute_values) == len(self.means) == len(self.scales)):
            raise ValueError("transform vector width mismatch")
        if any((not math.isfinite(v) or v <= 0) for v in self.scales):
            raise ValueError("invalid transform scale")
        expected = stable_id("xform", self.canonical())
        if self.transform_hash and self.transform_hash != expected:
            raise ValueError("transform-state hash mismatch")

@dataclass(frozen=True, slots=True)
class TrainingPlan:
    plan_id: str
    plan_version: str
    task: TaskKind
    dataset_hash: str
    feature_schema_hash: str
    label_contract_hash: str
    model_families: tuple[ModelFamily, ...]
    transform_spec_hash: str
    calibration_method: CalibrationMethod
    selection_metric: str
    random_seed: int = 130013
    maximum_iterations: int = 500
    learning_rate: float = 0.05
    l2_penalty: float = 0.01
    threshold_grid_size: int = 32
    plan_hash: str = ""

    def canonical(self) -> str:
        families = ",".join(str(int(v)) for v in self.model_families)
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/training_plan@1.0.0", self.plan_id,
            self.plan_version, int(self.task), self.dataset_hash, self.feature_schema_hash,
            self.label_contract_hash, families, self.transform_spec_hash,
            int(self.calibration_method), self.selection_metric, self.random_seed,
            self.maximum_iterations, cfloat(self.learning_rate), cfloat(self.l2_penalty),
            self.threshold_grid_size]))

    def with_hash(self) -> "TrainingPlan":
        return type(self)(**{**asdict(self), "task": self.task, "model_families": self.model_families,
            "calibration_method": self.calibration_method, "plan_hash": stable_id("tplan", self.canonical())})

    def validate(self) -> None:
        _required(self.plan_id, self.plan_version, self.dataset_hash, self.feature_schema_hash,
                  self.label_contract_hash, self.transform_spec_hash, self.selection_metric)
        if not self.model_families or len(set(self.model_families)) != len(self.model_families):
            raise ValueError("training plan needs unique model families")
        if self.maximum_iterations < 1 or self.maximum_iterations > 1_000_000:
            raise ValueError("invalid iteration bound")
        if self.learning_rate <= 0 or self.l2_penalty < 0 or self.threshold_grid_size < 2:
            raise ValueError("invalid optimizer or threshold configuration")
        expected = stable_id("tplan", self.canonical())
        if self.plan_hash and self.plan_hash != expected:
            raise ValueError("training-plan hash mismatch")

@dataclass(frozen=True, slots=True)
class ModelArtifact:
    model_id: str
    model_version: str
    family: ModelFamily
    task: TaskKind
    training_plan_hash: str
    dataset_hash: str
    feature_schema_hash: str
    label_contract_hash: str
    transform_hash: str
    training_rowset_hash: str
    parameter_names: tuple[str, ...]
    parameter_values: tuple[float, ...]
    selected_on_role: DatasetRole
    random_seed: int
    no_execution_authority: bool = True
    artifact_hash: str = ""

    def canonical(self) -> str:
        parameters = ",".join(f"{n}={cfloat(v)}" for n, v in zip(self.parameter_names, self.parameter_values))
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/model_artifact@1.0.0", self.model_id,
            self.model_version, int(self.family), int(self.task), self.training_plan_hash,
            self.dataset_hash, self.feature_schema_hash, self.label_contract_hash, self.transform_hash,
            self.training_rowset_hash, parameters, int(self.selected_on_role), self.random_seed,
            cbool(self.no_execution_authority)]))

    def with_hash(self) -> "ModelArtifact":
        return type(self)(**{**asdict(self), "family": self.family, "task": self.task,
            "parameter_names": self.parameter_names, "parameter_values": self.parameter_values,
            "selected_on_role": self.selected_on_role,
            "artifact_hash": stable_id("model", self.canonical())})

    def validate(self) -> None:
        _required(self.model_id, self.model_version, self.training_plan_hash, self.dataset_hash,
                  self.feature_schema_hash, self.label_contract_hash, self.transform_hash,
                  self.training_rowset_hash)
        if len(self.parameter_names) != len(self.parameter_values) or len(set(self.parameter_names)) != len(self.parameter_names):
            raise ValueError("invalid model parameter packet")
        if self.selected_on_role != DatasetRole.VALIDATION:
            raise ValueError("model must be selected on validation evidence")
        if not self.no_execution_authority:
            raise ValueError("Phase 13 model artifact cannot carry execution authority")
        expected = stable_id("model", self.canonical())
        if self.artifact_hash and self.artifact_hash != expected:
            raise ValueError("model-artifact hash mismatch")

@dataclass(frozen=True, slots=True)
class CalibrationArtifact:
    calibration_id: str
    method: CalibrationMethod
    model_artifact_hash: str
    validation_rowset_hash: str
    intercept: float
    slope: float
    sample_count: int
    calibration_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/calibration_artifact@1.0.0",
            self.calibration_id, int(self.method), self.model_artifact_hash,
            self.validation_rowset_hash, cfloat(self.intercept), cfloat(self.slope), self.sample_count]))

    def with_hash(self) -> "CalibrationArtifact":
        return type(self)(**{**asdict(self), "method": self.method,
            "calibration_hash": stable_id("cal", self.canonical())})

@dataclass(frozen=True, slots=True)
class PredictionRecord:
    model_artifact_hash: str
    calibration_hash: str
    dataset_hash: str
    row_id: str
    fold_id: str
    role: PredictionRole
    raw_score: float
    probability: float
    action_score: float
    generated_at_utc_msc: int
    prediction_id: str = ""
    prediction_hash: str = ""

    def canonical_identity(self) -> str:
        return "|".join(map(str, [self.model_artifact_hash, self.dataset_hash, self.row_id,
            self.fold_id, int(self.role)]))

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/prediction_record@1.0.0",
            self.prediction_id, self.canonical_identity(), self.calibration_hash,
            cfloat(self.raw_score), cfloat(self.probability), cfloat(self.action_score),
            self.generated_at_utc_msc]))

    def with_hashes(self) -> "PredictionRecord":
        pid = self.prediction_id or stable_id("pred", self.canonical_identity())
        candidate = type(self)(**{**asdict(self), "role": self.role, "prediction_id": pid,
            "prediction_hash": ""})
        return type(self)(**{**asdict(candidate), "role": candidate.role,
            "prediction_hash": stable_id("predh", candidate.canonical())})

    def validate(self) -> None:
        _required(self.model_artifact_hash, self.dataset_hash, self.row_id, self.fold_id)
        if not all(math.isfinite(v) for v in (self.raw_score, self.probability, self.action_score)):
            raise ValueError("non-finite prediction")
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability outside unit interval")
        if self.role != PredictionRole.TEST_OOS:
            raise ValueError("published Phase 13 predictions must be test OOS")
        expected_id = stable_id("pred", self.canonical_identity())
        if self.prediction_id and self.prediction_id != expected_id:
            raise ValueError("prediction identity mismatch")

@dataclass(frozen=True, slots=True)
class ModelCard:
    model_artifact_hash: str
    training_plan_hash: str
    dataset_hash: str
    selection_metric: str
    validation_score: float
    test_score: float
    test_sample_count: int
    calibration_hash: str
    intended_use: str
    limitations: tuple[str, ...]
    status: TrainingStatus
    no_capital_authority: bool = True
    card_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/model_card@1.0.0",
            self.model_artifact_hash, self.training_plan_hash, self.dataset_hash,
            self.selection_metric, cfloat(self.validation_score), cfloat(self.test_score),
            self.test_sample_count, self.calibration_hash, self.intended_use,
            "||".join(self.limitations), int(self.status), cbool(self.no_capital_authority)]))

    def with_hash(self) -> "ModelCard":
        return type(self)(**{**asdict(self), "limitations": self.limitations, "status": self.status,
            "card_hash": stable_id("mcard", self.canonical())})

@dataclass(frozen=True, slots=True)
class TrainingReportManifest:
    report_id: str
    training_plan_hash: str
    dataset_hash: str
    model_artifact_hash: str
    calibration_hash: str
    prediction_rowset_hash: str
    model_card_hash: str
    candidate_count: int
    selected_family: ModelFamily
    status: TrainingStatus
    generated_at_utc_msc: int
    report_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/training_report_manifest@1.0.0",
            self.report_id, self.training_plan_hash, self.dataset_hash, self.model_artifact_hash,
            self.calibration_hash, self.prediction_rowset_hash, self.model_card_hash,
            self.candidate_count, int(self.selected_family), int(self.status),
            self.generated_at_utc_msc]))

    def with_hash(self) -> "TrainingReportManifest":
        return type(self)(**{**asdict(self), "selected_family": self.selected_family,
            "status": self.status, "report_hash": stable_id("trep", self.canonical())})
