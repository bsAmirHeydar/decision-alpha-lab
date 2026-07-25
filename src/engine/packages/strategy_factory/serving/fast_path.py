"""Compiled, bounded, in-memory context-to-decision fast path."""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Any, Mapping, Sequence

from ..context.engine import IncrementalContextEngine
from ..contracts import AnatomyEvent, stable_hash
from ..decision.models import ModelRoute
from ..decision.policy import ThresholdDecisionPolicy
from ..decision.scoring import score_candidates
from ..optimization.plan import CompiledStrategyPlan
from ..runtime.dedup import IdempotencyGuard
from ..runtime.latency import LatencyTracker
from ..runtime.telemetry import DecisionTelemetry, TelemetryBuffer
from .candidates import CompiledCandidateFactory
from .fallback import abstain_envelope


class FastDecisionEngine:
    """Reference online engine.

    All dynamic work (manifest parsing, plugin discovery, dependency sorting,
    candidate Cartesian products) must be completed before this object is used.
    The decision path performs bounded computation and no file/network I/O.
    """

    __slots__ = (
        "plan",
        "context_engine",
        "candidate_factory",
        "decision_policy",
        "telemetry",
        "dedup",
        "pre_gates",
        "_model_bindings",
    )

    def __init__(
        self,
        plan: CompiledStrategyPlan,
        context_engine: IncrementalContextEngine,
        candidate_factory: CompiledCandidateFactory,
        decision_policy: ThresholdDecisionPolicy,
        *,
        telemetry: TelemetryBuffer | None = None,
        dedup: IdempotencyGuard | None = None,
        pre_gates: Sequence[Any] = (),
    ) -> None:
        self.plan = plan
        self.context_engine = context_engine
        self.candidate_factory = candidate_factory
        self.decision_policy = decision_policy
        self.telemetry = telemetry or TelemetryBuffer()
        self.dedup = dedup or IdempotencyGuard()
        self.pre_gates = tuple(pre_gates)
        self._model_bindings = tuple(
            (
                route,
                self.plan.plugin_registry.resolve("model", route.model_id, route.model_version),
                self.plan.feature_schemas.get(route.feature_schema_id),
            )
            for route in self.plan.model_routes
        )
        for route, model, schema in self._model_bindings:
            if schema is None and route.required:
                raise KeyError(f"missing feature schema {route.feature_schema_id}")

    def decide(
        self,
        event: AnatomyEvent,
        market_state: Mapping[str, Any],
        decision_time_utc: datetime,
        *,
        state_generation: int = 0,
        base_context: Mapping[str, Any] | None = None,
    ):
        tracker = LatencyTracker()
        event.validate()
        idempotency_key = f"{self.plan.plan_hash}:{event.event_id}:{decision_time_utc.isoformat()}"
        if not self.dedup.claim(idempotency_key):
            return abstain_envelope(
                event,
                (),
                decision_time_utc,
                reason_codes=("duplicate_decision_request",),
                plan_hash=self.plan.plan_hash,
            )

        tracker.start("context")
        try:
            context_result = self.context_engine.build(
                event,
                market_state,
                decision_time_utc,
                state_generation=state_generation,
                base_context=base_context,
            )
        except Exception as exc:
            report = tracker.report(self.plan.latency_budget)
            return abstain_envelope(
                event,
                (),
                decision_time_utc,
                reason_codes=(f"context_error:{type(exc).__name__}",),
                plan_hash=self.plan.plan_hash,
                latency_ns={**report.stages_ns, "total": report.total_ns},
            )
        tracker.stop("context")
        context = context_result.flat
        context_hash = stable_hash(
            {"event_id": event.event_id, "context": context, "schema": context_result.snapshot.schema_version},
            prefix="ctx_",
        )
        if context_result.missing_required:
            report = tracker.report(self.plan.latency_budget)
            return abstain_envelope(
                event,
                (),
                decision_time_utc,
                reason_codes=("missing_required_features:" + ",".join(context_result.missing_required),),
                plan_hash=self.plan.plan_hash,
                context_hash=context_hash,
                latency_ns={**report.stages_ns, "total": report.total_ns},
            )

        tracker.start("pre_gates")
        for gate in self.pre_gates:
            approved, reason = gate.evaluate(event, context, decision_time_utc)
            if not approved:
                tracker.stop("pre_gates")
                report = tracker.report(self.plan.latency_budget)
                return abstain_envelope(
                    event,
                    (),
                    decision_time_utc,
                    reason_codes=(reason or f"gate_rejected:{gate.descriptor.plugin_id}",),
                    plan_hash=self.plan.plan_hash,
                    context_hash=context_hash,
                    latency_ns={**report.stages_ns, "total": report.total_ns},
                )
        tracker.stop("pre_gates")

        tracker.start("candidates")
        candidates = self.candidate_factory.build(event, context)
        tracker.stop("candidates")
        if not candidates:
            report = tracker.report(self.plan.latency_budget)
            return abstain_envelope(
                event,
                (),
                decision_time_utc,
                reason_codes=("no_eligible_candidates",),
                plan_hash=self.plan.plan_hash,
                context_hash=context_hash,
                latency_ns={**report.stages_ns, "total": report.total_ns},
            )

        tracker.start("models")
        outputs_by_candidate: dict[str, dict[str, float]] = {}
        for candidate in candidates:
            candidate_context = dict(context)
            candidate_context.update(
                {
                    "entry_price": candidate.entry_price,
                    "stop_price": candidate.stop_price,
                    "target_price": candidate.target_price or candidate.entry_price,
                    "risk_distance": candidate.risk_distance,
                }
            )
            aggregated: dict[str, float] = {}
            for route, model, schema in self._model_bindings:
                assert isinstance(route, ModelRoute)
                if schema is None:
                    continue
                vector = schema.encode(candidate_context, strict=route.required)
                raw = model.predict_one(vector)
                for target_name, source_name in route.output_mapping.items():
                    if source_name in raw:
                        aggregated[target_name] = float(raw[source_name])
                aggregated.setdefault("model_id", route.model_id)  # type: ignore[arg-type]
                aggregated.setdefault("model_version", model.descriptor.version)  # type: ignore[arg-type]
            outputs_by_candidate[candidate.candidate_id] = aggregated
        tracker.stop("models")

        tracker.start("ranking")
        scores = score_candidates(candidates, outputs_by_candidate, weights=self.plan.utility_weights)
        tracker.stop("ranking")

        interim_report = tracker.report(self.plan.latency_budget)
        envelope = self.decision_policy.decide(
            event,
            candidates,
            scores,
            context,
            decision_time_utc,
            plan_hash=self.plan.plan_hash,
            context_hash=context_hash,
            latency_ns={**interim_report.stages_ns, "total": interim_report.total_ns},
        )
        final_report = tracker.report(self.plan.latency_budget)
        if final_report.breaches and self.plan.latency_budget.action_on_breach == "abstain":
            envelope = abstain_envelope(
                event,
                candidates,
                decision_time_utc,
                reason_codes=("latency_budget_breach:" + ",".join(final_report.breaches),),
                plan_hash=self.plan.plan_hash,
                context_hash=context_hash,
                latency_ns={**final_report.stages_ns, "total": final_report.total_ns},
            )
        else:
            envelope = replace(
                envelope,
                latency_ns={**final_report.stages_ns, "total": final_report.total_ns},
                diagnostics={
                    "cache_hits": context_result.cache_hits,
                    "cache_misses": context_result.cache_misses,
                    "latency_breaches": final_report.breaches,
                },
            )
        self.telemetry.append(
            DecisionTelemetry(
                event_id=event.event_id,
                strategy_id=event.strategy_id,
                status=envelope.status.value,
                total_latency_ns=final_report.total_ns,
                stage_latency_ns=final_report.stages_ns,
                cache_hits=context_result.cache_hits,
                cache_misses=context_result.cache_misses,
                candidate_count=len(candidates),
                reason_codes=envelope.reason_codes,
                plan_hash=self.plan.plan_hash,
            )
        )
        return envelope
