"""Closed enumerations used by SAED V4-00 contracts."""
from __future__ import annotations
from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class DecisionStatus(StrEnum):
    ALLOW = "allow"
    REJECT = "reject"
    QUARANTINE = "quarantine"
    REQUIRE_REVIEW = "require_review"


class ClaimClass(StrEnum):
    DESCRIPTIVE = "descriptive"
    ASSOCIATIONAL = "associational"
    CAUSAL = "causal"
    PREDICTIVE = "predictive"
    DECISION_THEORETIC = "decision_theoretic"
    STRESS_ONLY = "stress_only"
    OPERATIONAL = "operational"


class EvidenceRole(StrEnum):
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


class EvidenceOperation(StrEnum):
    TRAIN = "train"
    TUNE = "tune"
    CALIBRATE = "calibrate"
    SELECT = "select"
    REPORT = "report"
    PROMOTE = "promote"
    STRESS = "stress"
    REPLAY = "replay"


class Authority(StrEnum):
    CONTEXT_TRUTH_MUTATION = "context_truth_mutation"
    EVIDENCE_ROLE_REASSIGNMENT = "evidence_role_reassignment"
    HIDDEN_EVALUATION_ROW_ACCESS = "hidden_evaluation_row_access"
    CONSTITUTION_SELF_AMENDMENT = "constitution_self_amendment"
    PROMOTION_SIGNATURE = "promotion_signature"
    RISK_LIMIT_CHANGE = "risk_limit_change"
    PORTFOLIO_ALLOCATION = "portfolio_allocation"
    RUNTIME_ACTIVATION = "runtime_activation"
    ORDER = "order"
    BROKER = "broker"
    NETWORK = "network"
    RESEARCH_PROPOSAL = "research_proposal"
    SANDBOX_COMPUTE = "sandbox_compute"
    EVIDENCE_PACKET_DRAFT = "evidence_packet_draft"
    RED_TEAM_CHALLENGE = "red_team_challenge"
    INDEPENDENT_REVIEW = "independent_review"


class ActorType(StrEnum):
    HUMAN_RESEARCHER = "human_researcher"
    HUMAN_REVIEWER = "human_reviewer"
    RISK_COMMITTEE = "risk_committee"
    AGENT = "agent"
    HIDDEN_EVALUATION_SERVICE = "hidden_evaluation_service"
    RUNTIME_COMPILER = "runtime_compiler"
    PORTFOLIO_ENGINE = "portfolio_engine"
    EXECUTION_ADAPTER = "execution_adapter"


class AmendmentStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"


class WaiverStatus(StrEnum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ExposureKind(StrEnum):
    TRIAL = "trial"
    QUERY = "query"
    CHART = "chart"
    DASHBOARD = "dashboard"
    NARRATIVE = "narrative"
    AGENT_SUGGESTION = "agent_suggestion"
    THRESHOLD_CHANGE = "threshold_change"
    FEATURE_PROPOSAL = "feature_proposal"
    HIDDEN_EVALUATION_SUBMISSION = "hidden_evaluation_submission"
    RESULT_SHARE = "result_share"


class ReasonCode(StrEnum):
    OK = "ok"
    UNKNOWN_FIELD = "unknown_field"
    INVALID_SCHEMA = "invalid_schema"
    AUTHORITY_DENIED = "authority_denied"
    PROTECTED_EVIDENCE_TRAINING = "protected_evidence_training"
    SYNTHETIC_POSITIVE_PROMOTION = "synthetic_positive_promotion"
    OBJECTIVE_CHANGE_REQUIRES_AMENDMENT = "objective_change_requires_amendment"
    RETROACTIVE_AMENDMENT = "retroactive_amendment"
    SELF_APPROVAL = "self_approval"
    REVIEWER_NOT_INDEPENDENT = "reviewer_not_independent"
    MISSING_SECOND_APPROVAL = "missing_second_approval"
    NON_WAIVABLE_RULE = "non_waivable_rule"
    WAIVER_EXPIRED = "waiver_expired"
    BASELINE_SET_INCOMPLETE = "baseline_set_incomplete"
    EXPOSURE_BUDGET_EXHAUSTED = "exposure_budget_exhausted"
    CORE_BOUNDARY_CHANGED = "core_boundary_changed"
    EXTERNAL_EVIDENCE_MISCLASSIFIED = "external_evidence_misclassified"
    LINEAGE_MISMATCH = "lineage_mismatch"
    LEDGER_CHAIN_BROKEN = "ledger_chain_broken"
    SIGNATURE_INVALID = "signature_invalid"
    KNOWN_TIME_REQUIRED = "known_time_required"
