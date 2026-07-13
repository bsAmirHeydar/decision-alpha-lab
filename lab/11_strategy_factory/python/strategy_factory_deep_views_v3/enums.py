"""Closed enumerations for UCE-I10."""

from enum import Enum


class DeepFamily(str, Enum):
    SEQUENCE = "sequence"
    VISION = "vision"
    GRAPH = "graph"
    REGIME_ANOMALY = "regime_anomaly"
    MULTI_VIEW_FUSION = "multi_view_fusion"
    TRANSFER_COMPRESSION = "transfer_compression"
    QUALIFICATION = "qualification"


class AdmissionDecision(str, Enum):
    ACCEPT = "accept"
    WARN = "warn"
    REJECT = "reject"


class MissingViewPolicy(str, Enum):
    REJECT = "reject"
    ABSTAIN = "abstain"
    ZERO_FILL = "zero_fill"
    GLOBAL_FALLBACK = "global_fallback"


class FusionKind(str, Enum):
    LATE_WEIGHTED = "late_weighted"
    GATED = "gated"
    STACKED = "stacked"


class ExportPath(str, Enum):
    NONE = "none"
    NATIVE_JSON = "native_json"
    ONNX = "onnx"
    DISTILLED_MQL5 = "distilled_mql5"


class QualificationDecision(str, Enum):
    PROMOTABLE = "promotable"
    CHALLENGER_ONLY = "challenger_only"
    REJECTED = "rejected"


class ViewStatus(str, Enum):
    AVAILABLE = "available"
    MISSING = "missing"
    STALE = "stale"
    INVALID = "invalid"


class RegimeGateDecision(str, Enum):
    EXPERT = "expert"
    GLOBAL = "global"
    ABSTAIN = "abstain"


class DependencyStatus(str, Enum):
    AVAILABLE = "available"
    MISSING = "missing"
    INCOMPATIBLE = "incompatible"


class TransferDecision(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
