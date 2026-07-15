from __future__ import annotations
from .contracts import ChaosReport, GateResult, QualificationPolicy
from .enums import EvidenceStatus, GateName


def evaluate_chaos(report: ChaosReport, policy: QualificationPolicy, evaluated_at_ms: int) -> GateResult:
    by_id = {item.scenario_id: item for item in report.scenarios}
    reasons = []
    if tuple(sorted(report.required_scenario_ids)) != tuple(sorted(policy.required_chaos_scenarios)):
        reasons.append("chaos_policy_contract_mismatch")
    for scenario_id in policy.required_chaos_scenarios:
        result = by_id.get(scenario_id)
        if result is None:
            reasons.append(f"missing_chaos_scenario:{scenario_id}")
        elif not result.passed:
            reasons.append(f"chaos_scenario_failed:{scenario_id}")
    return GateResult(GateName.CHAOS, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (report.report_hash,), evaluated_at_ms)
