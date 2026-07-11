"""Typed plugin interfaces for Strategy Factory V2.

The live fast path uses already-instantiated plugins. Dynamic discovery and
manifest parsing happen only during compilation/startup, never per decision.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

from ..contracts import AnatomyEvent, ExecutionIntent, FeatureValue, ModelDecision, TradeCandidate


@dataclass(frozen=True, slots=True)
class PluginDescriptor:
    plugin_id: str
    version: str
    kind: str
    deterministic: bool = True
    thread_safe: bool = True
    fast_path_safe: bool = True
    capabilities: tuple[str, ...] = ()


@runtime_checkable
class AnatomyPlugin(Protocol):
    descriptor: PluginDescriptor

    def emit(self, raw_event: Mapping[str, Any]) -> AnatomyEvent:
        ...


@runtime_checkable
class FeatureProvider(Protocol):
    descriptor: PluginDescriptor
    feature_names: tuple[str, ...]
    dependencies: tuple[str, ...]
    ttl_seconds: float | None
    required: bool

    def compute(
        self,
        event: AnatomyEvent,
        resolved: Mapping[str, Any],
        market_state: Mapping[str, Any],
        decision_time_utc: datetime,
    ) -> Sequence[FeatureValue]:
        ...


@runtime_checkable
class PreDecisionGate(Protocol):
    descriptor: PluginDescriptor

    def evaluate(
        self,
        event: AnatomyEvent,
        context: Mapping[str, Any],
        decision_time_utc: datetime,
    ) -> tuple[bool, str | None]:
        ...


@runtime_checkable
class CandidatePolicyPlugin(Protocol):
    descriptor: PluginDescriptor

    def build(
        self,
        event: AnatomyEvent,
        context: Mapping[str, Any],
        policy_parameters: Mapping[str, Any],
    ) -> TradeCandidate | None:
        ...


@runtime_checkable
class ModelPlugin(Protocol):
    descriptor: PluginDescriptor
    feature_order: tuple[str, ...]

    def predict_one(self, values: Sequence[float]) -> Mapping[str, float]:
        ...

    def predict_batch(self, rows: Sequence[Sequence[float]]) -> Sequence[Mapping[str, float]]:
        ...


@runtime_checkable
class DecisionPolicy(Protocol):
    descriptor: PluginDescriptor

    def decide(
        self,
        event: AnatomyEvent,
        candidates: Sequence[TradeCandidate],
        context: Mapping[str, Any],
        model_outputs: Mapping[str, Mapping[str, float]],
        decision_time_utc: datetime,
    ) -> ModelDecision:
        ...


@runtime_checkable
class RiskPolicyPlugin(Protocol):
    descriptor: PluginDescriptor

    def authorize(
        self,
        decision: ModelDecision,
        candidate: TradeCandidate | None,
        state: Mapping[str, Any],
    ) -> tuple[bool, str | None, float | None]:
        """Return approved, reason, and optional risk dollars."""
        ...


@runtime_checkable
class ExecutionAdapterPlugin(Protocol):
    descriptor: PluginDescriptor

    def submit(self, intent: ExecutionIntent) -> Mapping[str, Any]:
        ...
