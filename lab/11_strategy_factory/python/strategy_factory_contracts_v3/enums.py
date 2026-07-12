"""Closed vocabularies used by the UCEE v3 contract kernel."""
from enum import StrEnum

class IdentityKind(StrEnum):
    CONTEXT_OCCURRENCE="context_occurrence"
    CONTEXT_CLUSTER="context_cluster"
    PARENT_EVENT="parent_event"
    REPRESENTATION_VIEW="representation_view"
    TREATMENT_ATOM="treatment_atom"
    COMPLETE_TREATMENT="complete_treatment"
    TASK="task"
    DATASET_ROW="dataset_row"
    EXPERIMENT_TRIAL="experiment_trial"
    PREDICTION="prediction"
    MODEL="model"
    POLICY="policy"
    RUNTIME_GENERATION="runtime_generation"
    EVIDENCE_BUNDLE="evidence_bundle"

class RuntimeMode(StrEnum):
    RESEARCH="research"
    TESTER="tester"
    PAPER="paper"
    SHADOW="shadow"
    LIVE="live"

class TaskType(StrEnum):
    BINARY_CLASSIFICATION="binary_classification"
    MULTICLASS_CLASSIFICATION="multiclass_classification"
    REGRESSION="regression"
    QUANTILE_REGRESSION="quantile_regression"
    PAIRWISE_RANKING="pairwise_ranking"
    LISTWISE_RANKING="listwise_ranking"
    SURVIVAL="survival"
    POLICY_SELECTION="policy_selection"
    MULTI_TASK="multi_task"

class RepresentationKind(StrEnum):
    TABULAR="tabular"
    SEQUENCE="sequence"
    IMAGE="image"
    GRAPH="graph"
    MULTI_VIEW="multi_view"

class SupportLevel(StrEnum):
    EXPERIMENTAL="experimental"
    RESEARCH="research"
    PAPER="paper"
    PRODUCTION="production"

class CompatibilityStatus(StrEnum):
    COMPATIBLE="compatible"
    COMPATIBLE_AFTER_MIGRATION="compatible_after_migration"
    INCOMPATIBLE="incompatible"

class MigrationMode(StrEnum):
    LOSSLESS="lossless"
    LOSSY="lossy"
    SEMANTIC_REINTERPRETATION="semantic_reinterpretation"
