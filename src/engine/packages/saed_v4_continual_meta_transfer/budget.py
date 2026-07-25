from __future__ import annotations

from dataclasses import asdict

from .canonical import content_hash
from .contracts import ResearchBudget
from .errors import BudgetError


class ResearchLedger:
    _LIMIT_FIELDS = {
        "tasks": "maximum_tasks",
        "source_evaluations": "maximum_source_evaluations",
        "adaptations": "maximum_adaptations",
        "replay_entries": "maximum_replay_entries",
        "recalibration_trials": "maximum_recalibration_trials",
        "bootstrap_draws": "maximum_bootstrap_draws",
        "hidden_evaluation_queries": "maximum_hidden_evaluation_queries",
        "protected_evidence_exposures": "maximum_protected_evidence_exposures",
        "runtime_compilations": "maximum_runtime_compilations",
        "order_submissions": "maximum_order_submissions",
        "online_policy_mutations": "maximum_online_policy_mutations",
        "failures": "failure_budget",
    }

    def __init__(self, contract: ResearchBudget):
        self.contract = contract
        self.counts = {name: 0 for name in self._LIMIT_FIELDS}
        self.events: list[dict] = []

    def consume(self, name: str, amount: int = 1, reason: str = "") -> None:
        if name not in self._LIMIT_FIELDS:
            raise BudgetError(f"unknown budget counter {name}")
        amount = int(amount)
        if amount < 0:
            raise BudgetError("budget consumption cannot be negative")
        candidate = self.counts[name] + amount
        limit = int(getattr(self.contract, self._LIMIT_FIELDS[name]))
        if candidate > limit:
            raise BudgetError(f"budget exceeded for {name}: {candidate}>{limit}")
        self.counts[name] = candidate
        self.events.append({"counter": name, "amount": amount, "reason": str(reason), "after": candidate, "limit": limit})

    def snapshot(self) -> dict:
        limits = {
            name: int(getattr(self.contract, field))
            for name, field in self._LIMIT_FIELDS.items()
        }
        payload = {
            "phase": "SAED_V4_25",
            "counts": dict(self.counts),
            "limits": limits,
            "events": list(self.events),
            "complete": True,
            "within_budget": all(self.counts[name] <= limits[name] for name in limits),
        }
        payload["budget_hash"] = content_hash(payload)
        return payload
