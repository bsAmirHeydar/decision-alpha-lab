"""Authority matrix and constitutional authority evaluation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .enums import ActorType, Authority, DecisionStatus, ReasonCode
from .models import AuthorityRequest


HARD_DENIED_FOR_RESEARCH = frozenset({
    Authority.CONTEXT_TRUTH_MUTATION,
    Authority.EVIDENCE_ROLE_REASSIGNMENT,
    Authority.HIDDEN_EVALUATION_ROW_ACCESS,
    Authority.CONSTITUTION_SELF_AMENDMENT,
    Authority.PROMOTION_SIGNATURE,
    Authority.RISK_LIMIT_CHANGE,
    Authority.PORTFOLIO_ALLOCATION,
    Authority.RUNTIME_ACTIVATION,
    Authority.ORDER,
    Authority.BROKER,
    Authority.NETWORK,
})


DEFAULT_GRANTS: dict[ActorType, frozenset[Authority]] = {
    ActorType.HUMAN_RESEARCHER: frozenset({
        Authority.RESEARCH_PROPOSAL,
        Authority.SANDBOX_COMPUTE,
        Authority.EVIDENCE_PACKET_DRAFT,
    }),
    ActorType.HUMAN_REVIEWER: frozenset({
        Authority.INDEPENDENT_REVIEW,
        Authority.RED_TEAM_CHALLENGE,
    }),
    ActorType.AGENT: frozenset({
        Authority.RESEARCH_PROPOSAL,
        Authority.SANDBOX_COMPUTE,
        Authority.EVIDENCE_PACKET_DRAFT,
        Authority.RED_TEAM_CHALLENGE,
    }),
    ActorType.HIDDEN_EVALUATION_SERVICE: frozenset({
        Authority.HIDDEN_EVALUATION_ROW_ACCESS,
        Authority.EVIDENCE_PACKET_DRAFT,
    }),
    ActorType.RISK_COMMITTEE: frozenset({
        Authority.INDEPENDENT_REVIEW,
        Authority.PROMOTION_SIGNATURE,
        Authority.RISK_LIMIT_CHANGE,
    }),
    ActorType.RUNTIME_COMPILER: frozenset({Authority.RUNTIME_ACTIVATION}),
    ActorType.PORTFOLIO_ENGINE: frozenset({Authority.PORTFOLIO_ALLOCATION}),
    ActorType.EXECUTION_ADAPTER: frozenset({Authority.ORDER, Authority.BROKER, Authority.NETWORK}),
}


@dataclass(frozen=True)
class AuthorityEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]


class AuthorityMatrix:
    """Closed, explicit grants. Absence means deny."""

    def __init__(self, grants: dict[ActorType, Iterable[Authority]] | None = None) -> None:
        source = grants or DEFAULT_GRANTS
        self._grants = {k: frozenset(v) for k, v in source.items()}

    def granted(self, actor_type: ActorType) -> frozenset[Authority]:
        return self._grants.get(actor_type, frozenset())

    def evaluate(self, request: AuthorityRequest) -> AuthorityEvaluation:
        authority = request.authority
        actor_type = request.actor.actor_type

        if actor_type in {ActorType.AGENT, ActorType.HUMAN_RESEARCHER, ActorType.HUMAN_REVIEWER}:
            if authority in HARD_DENIED_FOR_RESEARCH:
                return AuthorityEvaluation(
                    DecisionStatus.REJECT,
                    (ReasonCode.AUTHORITY_DENIED,),
                    (f"{authority.value} is constitutionally denied to {actor_type.value}",),
                )

        if authority not in self.granted(actor_type):
            return AuthorityEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.AUTHORITY_DENIED,),
                (f"no explicit grant for {actor_type.value}:{authority.value}",),
            )

        # Specialized services remain purpose-limited.
        if actor_type == ActorType.HIDDEN_EVALUATION_SERVICE and authority == Authority.HIDDEN_EVALUATION_ROW_ACCESS:
            if "hidden_evaluation" not in request.purpose.lower():
                return AuthorityEvaluation(
                    DecisionStatus.REJECT,
                    (ReasonCode.AUTHORITY_DENIED,),
                    ("hidden row access requires hidden_evaluation purpose",),
                )

        return AuthorityEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), ())

    def to_dict(self) -> dict[str, list[str]]:
        return {k.value: sorted(x.value for x in v) for k, v in sorted(self._grants.items(), key=lambda item: item[0].value)}
