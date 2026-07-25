"""Closed enumerations for context packages, observations, features, views and clusters."""
from enum import Enum, IntFlag

class ContextLifecycleState(str, Enum):
    DETECTED="detected"; CONFIRMED="confirmed"; ACTIVE="active"; INVALIDATED="invalidated"; EXPIRED="expired"; SUPERSEDED="superseded"; RETIRED="retired"

class ContextUpdateScope(IntFlag):
    NONE=0; TICK=1; NEW_BAR=2; TIMER=4; REPLAY=8; HISTORY_REBUILD=16; MANUAL=32

class SourceRequirementKind(str, Enum):
    CLOSED_BARS="closed_bars"; TICKS="ticks"; SYMBOL_SPEC="symbol_spec"; ACCOUNT="account"; CALENDAR="calendar"; EXTERNAL_LEDGER="external_ledger"; ANATOMY_EVENT="anatomy_event"

class RequirementStrength(str, Enum): REQUIRED="required"; OPTIONAL="optional"
class FeatureDataType(str, Enum): BOOL="bool"; INT64="int64"; FLOAT64="float64"; CATEGORY="category"; STRING="string"; VECTOR_FLOAT64="vector_float64"
class MissingnessPolicy(str, Enum): REJECT="reject"; EXPLICIT_MISSING="explicit_missing"; ZERO_IS_VALID="zero_is_valid"; FORWARD_FILL_BOUNDED="forward_fill_bounded"; NOT_APPLICABLE="not_applicable"
class StalenessPolicy(str, Enum): REJECT="reject"; MARK_STALE="mark_stale"; ALLOW_WITH_AGE="allow_with_age"
class AvailabilityMode(IntFlag): NONE=0; RESEARCH=1; TESTER=2; PAPER=4; SHADOW=8; LIVE=16
class RepresentationKind(str, Enum):
    TABULAR="tabular"; SEQUENCE="sequence"; GRAPH="graph"; INTERMARKET="intermarket"; RASTER="raster"; SPARSE_EVENT="sparse_event"; PATH_SIGNATURE="path_signature"; EXECUTION="execution"; PORTFOLIO="portfolio"; FUSED="fused"
class ClusterKind(str, Enum):
    OPPORTUNITY="opportunity"; OVERLAPPING_PATH="overlapping_path"; PARENT_CHILD="parent_child"; SYMBOL_SESSION_DAY="symbol_session_day"; TREATMENT_SIBLING="treatment_sibling"; CUSTOM="custom"
class ManualPolicyKind(str, Enum): HARD_RULE="hard_rule"; BASELINE_SETUP="baseline_setup"; OVERRIDE="override"; ABSTENTION="abstention"; LABEL_ONLY="label_only"
class TaskKind(str, Enum): BINARY="binary"; MULTICLASS="multiclass"; REGRESSION="regression"; RANKING="ranking"; SURVIVAL="survival"; QUANTILE="quantile"; POLICY_SELECTION="policy_selection"
class FreshnessState(str, Enum): FRESH="fresh"; STALE="stale"; MISSING="missing"; INVALID="invalid"
class ConformanceSeverity(str, Enum): INFO="info"; WARNING="warning"; ERROR="error"; FATAL="fatal"
