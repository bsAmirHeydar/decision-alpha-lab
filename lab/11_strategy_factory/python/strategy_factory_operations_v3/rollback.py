from __future__ import annotations

from .contracts import DeploymentPlan, RollbackExecution
from .enums import ControlDecision


def evaluate_rollback(plan: DeploymentPlan, execution: RollbackExecution) -> tuple[ControlDecision, tuple[str, ...]]:
    reasons: list[str] = []
    if execution.plan_hash != plan.plan_hash:
        reasons.append("rollback_plan_mismatch")
    if execution.from_generation_hash != plan.generation_hash:
        reasons.append("rollback_source_generation_mismatch")
    if execution.to_generation_hash != plan.rollback_generation_hash:
        reasons.append("rollback_target_generation_mismatch")
    if execution.duration_seconds > execution.max_allowed_seconds:
        reasons.append("rollback_time_budget")
    if not execution.orders_blocked:
        reasons.append("orders_not_blocked")
    if not execution.positions_reconciled:
        reasons.append("positions_not_reconciled")
    if not execution.reservations_reconciled:
        reasons.append("reservations_not_reconciled")
    if not execution.target_generation_active:
        reasons.append("rollback_generation_not_active")
    return (ControlDecision.SAFE_HALT, tuple(sorted(set(reasons)))) if reasons else (ControlDecision.ROLLBACK, ())
