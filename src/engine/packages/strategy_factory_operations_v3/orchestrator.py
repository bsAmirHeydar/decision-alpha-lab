from __future__ import annotations

from .authorization import authorize_cycle
from .contracts import (
    CycleAuthorization,
    DeploymentPlan,
    OperationsIncident,
    OperationsPolicy,
    ReconciliationReport,
    RiskEnvelope,
    RuntimeLease,
    TelemetrySnapshot,
)
from .health import evaluate_health


def evaluate_operating_cycle(
    plan: DeploymentPlan,
    lease: RuntimeLease,
    telemetry: TelemetrySnapshot,
    reconciliation: ReconciliationReport,
    policy: OperationsPolicy,
    envelope: RiskEnvelope,
    evaluated_at_ms: int,
    incidents: tuple[OperationsIncident, ...] = (),
    manual_kill: bool = False,
) -> CycleAuthorization:
    health = evaluate_health(telemetry, policy, envelope, evaluated_at_ms)
    return authorize_cycle(plan, lease, health, reconciliation, policy, evaluated_at_ms, incidents, manual_kill)
