"""Startup-compiled candidate builders for the online path."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Mapping, Sequence

from ..candidate_engine import PolicyRegistry, default_registry
from ..contracts import AnatomyEvent, CandidateState, TradeCandidate, stable_hash
from ..optimization.plan import CandidateTemplate, CompiledStrategyPlan


@dataclass(frozen=True, slots=True)
class _CompiledTemplate:
    template: CandidateTemplate
    entry_policy: Any
    stop_policy: Any
    exit_policy: Any


class CompiledCandidateFactory:
    """Resolve policy callables once; build bounded candidates per event."""

    __slots__ = ("_templates", "_default_expiry", "_default_holding", "_cost_model_id", "_manifest_hash")

    def __init__(
        self,
        plan: CompiledStrategyPlan,
        *,
        policy_registry: PolicyRegistry | None = None,
        default_expiration_seconds: int = 3600,
        default_max_holding_seconds: int | None = None,
        cost_model_id: str = "default",
    ) -> None:
        registry = policy_registry or default_registry()
        compiled: list[_CompiledTemplate] = []
        for template in plan.candidate_templates:
            try:
                entry = registry.entries[template.entry_policy_id]
                stop = registry.stops[template.stop_policy_id]
                exit_policy = registry.exits[template.exit_policy_id]
            except KeyError as exc:
                raise KeyError(f"unregistered candidate policy in {template.template_id}: {exc}") from exc
            compiled.append(_CompiledTemplate(template, entry, stop, exit_policy))
        self._templates = tuple(compiled[: plan.max_candidates_per_event])
        self._default_expiry = int(default_expiration_seconds)
        self._default_holding = default_max_holding_seconds
        self._cost_model_id = cost_model_id
        self._manifest_hash = plan.plan_hash

    def build(self, event: AnatomyEvent, context: Mapping[str, Any]) -> tuple[TradeCandidate, ...]:
        candidates: list[TradeCandidate] = []
        for compiled in self._templates:
            template = compiled.template
            merged = dict(context)
            merged.update(template.parameters)
            entry_price = float(compiled.entry_policy.price_fn(event, merged))
            stop_price = float(compiled.stop_policy.price_fn(event, merged))
            risk_distance = abs(entry_price - stop_price)
            if risk_distance <= 0:
                continue
            target = compiled.exit_policy.target_fn(event, merged, entry_price, stop_price)
            payload = {
                "event_id": event.event_id,
                "template_id": template.template_id,
                "entry_price": entry_price,
                "stop_price": stop_price,
                "target_price": target,
                "parameters": template.parameters,
                "plan_hash": self._manifest_hash,
            }
            candidate = TradeCandidate(
                candidate_id=stable_hash(payload, prefix="cand_")[:40],
                event_id=event.event_id,
                symbol=event.symbol,
                direction=event.direction,
                entry_policy_id=template.entry_policy_id,
                stop_policy_id=template.stop_policy_id,
                exit_policy_id=template.exit_policy_id,
                created_time_utc=event.confirmation_time_utc,
                eligible_from_utc=event.confirmation_time_utc,
                expires_at_utc=event.confirmation_time_utc + timedelta(seconds=self._default_expiry),
                entry_type=compiled.entry_policy.entry_type,
                entry_price=entry_price,
                stop_price=stop_price,
                target_price=None if target is None else float(target),
                risk_distance=risk_distance,
                max_holding_seconds=self._default_holding,
                cost_model_id=self._cost_model_id,
                policy_parameters={"template_id": template.template_id, **dict(template.parameters)},
                state=CandidateState.ELIGIBLE,
            )
            candidate.validate()
            candidates.append(candidate)
        return tuple(candidates)
