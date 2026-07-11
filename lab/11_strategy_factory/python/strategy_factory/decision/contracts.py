"""Decision-layer contracts for low-latency context-to-action flow."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Mapping, Sequence

from ..contracts import AnatomyEvent, ModelDecision, TradeCandidate


class DecisionStatus(str, Enum):
    TRADE = "trade"
    SKIP = "skip"
    ABSTAIN = "abstain"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class CandidateScore:
    candidate_id: str
    expected_net_r: float
    probability_positive: float
    probability_target: float | None = None
    expected_mfe_r: float | None = None
    expected_mae_r: float | None = None
    uncertainty: float | None = None
    utility: float = 0.0
    model_id: str = ""
    model_version: str = ""


@dataclass(frozen=True, slots=True)
class DecisionEnvelope:
    event: AnatomyEvent
    candidates: tuple[TradeCandidate, ...]
    model_decision: ModelDecision
    status: DecisionStatus
    selected_candidate: TradeCandidate | None
    scores: tuple[CandidateScore, ...]
    created_time_utc: datetime
    reason_codes: tuple[str, ...] = ()
    context_hash: str = ""
    plan_hash: str = ""
    latency_ns: Mapping[str, int] = field(default_factory=dict)
    diagnostics: Mapping[str, object] = field(default_factory=dict)
