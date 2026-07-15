from __future__ import annotations

from .contracts import CycleAuthorization, DeploymentPlan, RuntimeLease
from .enums import ControlDecision, DeploymentStage
from .errors import OperationsError


def assert_authorization_is_bounded(auth: CycleAuthorization, plan: DeploymentPlan, lease: RuntimeLease) -> None:
    if auth.plan_hash != plan.plan_hash or auth.lease_hash != lease.lease_hash:
        raise OperationsError("authorization_lineage", "authorization lineage does not match plan and lease")
    if auth.max_incremental_risk_units > min(plan.max_risk_units, lease.max_risk_units):
        raise OperationsError("authorization_risk", "authorization exceeds plan or lease")
    if auth.authority_order and auth.decision is not ControlDecision.ALLOW_BOUNDED:
        raise OperationsError("authorization_decision", "order authority requires ALLOW_BOUNDED")
    if plan.stage in (DeploymentStage.PAPER, DeploymentStage.SHADOW, DeploymentStage.FROZEN) and auth.authority_order:
        raise OperationsError("no_send_authority", "paper, shadow and frozen stages cannot authorize orders")
