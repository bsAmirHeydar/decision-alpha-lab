"""Decision Alpha Lab Strategy Factory.

A reusable anatomy-to-research-to-execution platform.  Strategy-specific code
is restricted to anatomy adapters, feature providers, and policy plugins.
"""
from .contracts import (
    AnatomyEvent,
    CandidateState,
    ContractError,
    DecisionAction,
    Direction,
    ExecutionIntent,
    ExecutionTrace,
    FeatureSnapshot,
    FeatureValue,
    ModelDecision,
    OutcomeRecord,
    TradeCandidate,
)

__all__ = [
    "AnatomyEvent",
    "CandidateState",
    "ContractError",
    "DecisionAction",
    "Direction",
    "ExecutionIntent",
    "ExecutionTrace",
    "FeatureSnapshot",
    "FeatureValue",
    "ModelDecision",
    "OutcomeRecord",
    "TradeCandidate",
]
