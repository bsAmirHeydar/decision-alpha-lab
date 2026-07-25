"""Closed state-transition kernel for candidate, reference, WW, and quota machines."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, Mapping, TypeVar

from .canonical import canonical_sha256
from .enums import CandidateState, QuotaConsumptionPolicy, QuotaState, ReferenceState, WWState
from .errors import FPI02Error

StateT = TypeVar("StateT", bound=Enum)


@dataclass(frozen=True, slots=True)
class TransitionEvidence(Generic[StateT]):
    machine: str
    subject_id: str
    previous_state: StateT
    next_state: StateT
    event_id: str
    occurred_utc_ms: int
    reason_code: str
    transition_version: str = "1.0.0"

    @property
    def transition_id(self) -> str:
        return "FPTRANS_" + canonical_sha256(self)[:32]


CANDIDATE_TRANSITIONS: Mapping[CandidateState, frozenset[CandidateState]] = {
    CandidateState.OBSERVED: frozenset({CandidateState.RAW_CANDIDATE, CandidateState.INVALID_DATA}),
    CandidateState.RAW_CANDIDATE: frozenset({CandidateState.CONFIRMED, CandidateState.CANCELLED_SECOND_TOUCH, CandidateState.EXPIRED_SESSION_DEADLINE, CandidateState.INVALID_DATA}),
    CandidateState.CONFIRMED: frozenset(),
    CandidateState.CANCELLED_SECOND_TOUCH: frozenset(),
    CandidateState.EXPIRED_SESSION_DEADLINE: frozenset(),
    CandidateState.INVALID_DATA: frozenset(),
}

REFERENCE_TRANSITIONS: Mapping[ReferenceState, frozenset[ReferenceState]] = {
    ReferenceState.FRESH: frozenset({ReferenceState.HUNTER_SEEN, ReferenceState.CONSUMED_BY_PROTECTED_TOUCH, ReferenceState.EXPIRED, ReferenceState.SUPERSEDED}),
    ReferenceState.HUNTER_SEEN: frozenset({ReferenceState.CONSUMED_BY_PROTECTED_TOUCH, ReferenceState.EXPIRED, ReferenceState.SUPERSEDED}),
    ReferenceState.CONSUMED_BY_PROTECTED_TOUCH: frozenset({ReferenceState.EXPIRED, ReferenceState.SUPERSEDED}),
    ReferenceState.EXPIRED: frozenset(),
    ReferenceState.SUPERSEDED: frozenset(),
}

WW_TRANSITIONS: Mapping[WWState, frozenset[WWState]] = {
    WWState.RAW: frozenset({WWState.CONFIRMED, WWState.INVALID_DATA, WWState.EXPIRED}),
    WWState.CONFIRMED: frozenset({WWState.NEUTRALIZED, WWState.EXPIRED}),
    WWState.NEUTRALIZED: frozenset({WWState.EXPIRED}),
    WWState.EXPIRED: frozenset(),
    WWState.INVALID_DATA: frozenset(),
}

QUOTA_TRANSITIONS: Mapping[QuotaState, frozenset[QuotaState]] = {
    QuotaState.AVAILABLE: frozenset({QuotaState.RESERVED}),
    QuotaState.RESERVED: frozenset({QuotaState.CONSUMED, QuotaState.RELEASED}),
    QuotaState.CONSUMED: frozenset(),
    QuotaState.RELEASED: frozenset(),
}


class StateMachine(Generic[StateT]):
    def __init__(self, name: str, transitions: Mapping[StateT, frozenset[StateT]]) -> None:
        self.name = name
        self.transitions = transitions

    def can_transition(self, previous: StateT, next_state: StateT) -> bool:
        return next_state in self.transitions.get(previous, frozenset())

    def transition(
        self,
        subject_id: str,
        previous: StateT,
        next_state: StateT,
        event_id: str,
        occurred_utc_ms: int,
        reason_code: str,
        quota_consumption_policy: QuotaConsumptionPolicy = QuotaConsumptionPolicy.UNSET,
    ) -> TransitionEvidence[StateT]:
        if not self.can_transition(previous, next_state):
            raise FPI02Error(
                "FP_RC_ILLEGAL_TRANSITION",
                f"illegal {self.name} transition {previous.value}->{next_state.value}",
                {"machine": self.name, "subject_id": subject_id},
            )
        if self.name == "quota" and next_state is QuotaState.CONSUMED and quota_consumption_policy is QuotaConsumptionPolicy.UNSET:
            raise FPI02Error("FP_RC_OPEN_DECISION_BLOCKS_LIVE", "quota consumption is forbidden while FP-DEC-012 is open")
        if occurred_utc_ms < 0 or not subject_id or not event_id or not reason_code:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "transition evidence fields are invalid")
        return TransitionEvidence(self.name, subject_id, previous, next_state, event_id, occurred_utc_ms, reason_code)


CANDIDATE_MACHINE = StateMachine("candidate", CANDIDATE_TRANSITIONS)
REFERENCE_MACHINE = StateMachine("reference_side", REFERENCE_TRANSITIONS)
WW_MACHINE = StateMachine("ww", WW_TRANSITIONS)
QUOTA_MACHINE = StateMachine("quota", QUOTA_TRANSITIONS)
