"""Strategy and model promotion gates."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    passed: bool
    observed: Any
    required: Any
    reason: str
    severity: str = "hard"


@dataclass(frozen=True)
class PromotionDecision:
    strategy_id: str
    from_state: str
    requested_state: str
    approved: bool
    gate_results: Sequence[GateResult]
    residual_risks: Sequence[str] = field(default_factory=tuple)


DEFAULT_STATE_ORDER = [
    "draft",
    "anatomy_defined",
    "dataset_ready",
    "baseline_tested",
    "oos_validated",
    "paper_ready",
    "paper_running",
    "micro_live",
    "live_approved",
    "scaled",
    "retired",
]


def evaluate_promotion(
    *,
    strategy_id: str,
    from_state: str,
    requested_state: str,
    evidence: Mapping[str, Any],
    requirements: Mapping[str, Any],
) -> PromotionDecision:
    if from_state not in DEFAULT_STATE_ORDER or requested_state not in DEFAULT_STATE_ORDER:
        raise ValueError("unknown lifecycle state")
    if requested_state != "retired":
        current_index = DEFAULT_STATE_ORDER.index(from_state)
        requested_index = DEFAULT_STATE_ORDER.index(requested_state)
        if requested_index != current_index + 1:
            raise ValueError("promotion may advance only one lifecycle state at a time")

    gates = []
    for key, required in requirements.items():
        observed = evidence.get(key)
        if isinstance(required, Mapping):
            operator = required.get("operator", ">=")
            threshold = required.get("value")
            if operator == ">=":
                passed = observed is not None and observed >= threshold
            elif operator == "<=":
                passed = observed is not None and observed <= threshold
            elif operator == "==":
                passed = observed == threshold
            elif operator == "in":
                passed = observed in threshold
            else:
                raise ValueError(f"unsupported gate operator: {operator}")
        else:
            threshold = required
            passed = observed == threshold
        gates.append(
            GateResult(
                gate_id=key,
                passed=bool(passed),
                observed=observed,
                required=required,
                reason="requirement satisfied" if passed else "requirement not satisfied",
            )
        )
    approved = all(gate.passed or gate.severity != "hard" for gate in gates)
    return PromotionDecision(
        strategy_id=strategy_id,
        from_state=from_state,
        requested_state=requested_state,
        approved=approved,
        gate_results=tuple(gates),
        residual_risks=tuple(evidence.get("residual_risks", ())),
    )
