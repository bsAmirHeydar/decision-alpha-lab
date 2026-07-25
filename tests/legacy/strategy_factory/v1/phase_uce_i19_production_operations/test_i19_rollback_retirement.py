from dataclasses import replace
import pytest
from strategy_factory_operations_v3.contracts import RollbackExecution
from strategy_factory_operations_v3.enums import ControlDecision
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.golden import H1, H2, H3, H4, NOW
from strategy_factory_operations_v3.retirement import compile_retirement_manifest
from strategy_factory_operations_v3.rollback import evaluate_rollback


def execution(plan, **changes):
    values = dict(rollback_id="r", plan_hash=plan.plan_hash, from_generation_hash=plan.generation_hash, to_generation_hash=plan.rollback_generation_hash, initiated_at_ms=NOW, completed_at_ms=NOW+1000, max_allowed_seconds=2, orders_blocked=True, positions_reconciled=True, reservations_reconciled=True, target_generation_active=True, evidence_hashes=(H1,))
    values.update(changes); return RollbackExecution(**values)


def test_clean_rollback_is_accepted(live_plan):
    assert evaluate_rollback(live_plan, execution(live_plan)) == (ControlDecision.ROLLBACK, ())


@pytest.mark.parametrize("changes,reason", [
    ({"plan_hash": H2}, "rollback_plan_mismatch"),
    ({"from_generation_hash": H2}, "rollback_source_generation_mismatch"),
    ({"to_generation_hash": H3}, "rollback_target_generation_mismatch"),
    ({"completed_at_ms": NOW+3000}, "rollback_time_budget"),
    ({"orders_blocked": False}, "orders_not_blocked"),
    ({"positions_reconciled": False}, "positions_not_reconciled"),
    ({"reservations_reconciled": False}, "reservations_not_reconciled"),
    ({"target_generation_active": False}, "rollback_generation_not_active"),
])
def test_rollback_failures_halt(live_plan, changes, reason):
    decision, reasons = evaluate_rollback(live_plan, execution(live_plan, **changes))
    assert decision is ControlDecision.SAFE_HALT and reason in reasons


def retire(plan, **kw):
    args = dict(release_manifest_hash=H1, retired_at_ms=NOW, retired_by="operator", approved_by="approver", positions_flat=True, reservations_zero=True, leases_revoked=True, evidence_archive_hash=H2, retention_until_ms=NOW+1000, reason="superseded")
    args.update(kw); return compile_retirement_manifest(plan, **args)


def test_retirement_manifest_requires_safe_terminal_state(live_plan):
    result = retire(live_plan)
    assert result.positions_flat and result.reservations_zero and result.leases_revoked


@pytest.mark.parametrize("field", ["positions_flat", "reservations_zero", "leases_revoked"])
def test_retirement_blocks_incomplete_safety_state(live_plan, field):
    with pytest.raises(OperationsError): retire(live_plan, **{field:False})


def test_retirement_blocks_material_open_incident(live_plan):
    with pytest.raises(OperationsError, match="retirement_incident"): retire(live_plan, open_high_or_critical_incidents=1)


def test_retirement_requires_separation_of_duties(live_plan):
    with pytest.raises(OperationsError): retire(live_plan, retired_by="same", approved_by="same")
