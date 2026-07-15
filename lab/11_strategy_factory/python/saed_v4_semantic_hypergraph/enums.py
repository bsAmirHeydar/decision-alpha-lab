from enum import Enum


class EvidenceRole(str, Enum):
    DEVELOPMENT = "development"
    CALIBRATION = "calibration"
    SELECTION_VALIDATION = "selection_validation"
    LOCKED_FINAL = "locked_final"
    PROSPECTIVE = "prospective"
    SHADOW = "shadow"
    MICRO_LIVE = "micro_live"
    LIVE = "live"
    SYNTHETIC_STRESS = "synthetic_stress"
    EXTERNAL_STATIC = "external_static"
    EXTERNAL_ACTUAL = "external_actual"


class NodeKind(str, Enum):
    CONTEXT = "context"
    VIEW = "view"
    FEATURE = "feature"
    SOURCE_ARTIFACT = "source_artifact"
    TEMPORAL_ANCHOR = "temporal_anchor"
    EXTERNAL_CONTEXT_REFERENCE = "external_context_reference"
    TREATMENT_DESCRIPTOR = "treatment_descriptor"


class RelationKind(str, Enum):
    CONTEXT_COMPOSITION = "context_composition"
    VIEW_COMPOSITION = "view_composition"
    SOURCE_PROVENANCE = "source_provenance"
    TEMPORAL_COHORT = "temporal_cohort"
    CROSS_VIEW_ALIGNMENT = "cross_view_alignment"
    SEMANTIC_FAMILY = "semantic_family"
    CONTEXT_ANCESTRY = "context_ancestry"
    TREATMENT_DESCRIPTOR_BINDING = "treatment_descriptor_binding"


class GraphStatus(str, Enum):
    COMPLETE = "complete"
    DEGRADED = "degraded"
    UNSUPPORTED = "unsupported"
    QUARANTINED = "quarantined"


class SupportStatus(str, Enum):
    SUPPORTED = "supported"
    DEGRADED = "degraded"
    UNSUPPORTED = "unsupported"


class ProjectionKind(str, Enum):
    INCIDENCE = "incidence"


class QueryDirection(str, Enum):
    INCIDENT = "incident"
