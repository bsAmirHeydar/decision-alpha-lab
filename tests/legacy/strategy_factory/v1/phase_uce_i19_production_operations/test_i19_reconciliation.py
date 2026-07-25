import pytest
from strategy_factory_operations_v3.enums import EvidenceState
from strategy_factory_operations_v3.golden import H2, H3, H4, NOW, policy, reconciliation
from strategy_factory_operations_v3.reconciliation import reconciliation_status


def status(**changes): return reconciliation_status(reconciliation(**changes), H2, H3, NOW, policy().max_reconciliation_age_ms)


def test_exact_reconciliation_passes():
    assert status() == (EvidenceState.PASS, ())


@pytest.mark.parametrize("changes,reason", [
    ({"environment_hash": H4}, "reconciliation_environment_mismatch"),
    ({"generation_hash": H4}, "reconciliation_generation_mismatch"),
    ({"reconciled_at_ms": NOW+1}, "reconciliation_from_future"),
    ({"reconciled_at_ms": NOW-policy().max_reconciliation_age_ms-1}, "reconciliation_stale"),
    ({"observed_reservation_hash": H4}, "reservation_hash_mismatch"),
    ({"observed_order_hash": H4}, "order_hash_mismatch"),
    ({"observed_position_hash": H4}, "position_hash_mismatch"),
    ({"orphan_order_count": 1}, "orphan_order_count"),
    ({"orphan_position_count": 1}, "orphan_position_count"),
    ({"missing_order_count": 1}, "missing_order_count"),
    ({"missing_position_count": 1}, "missing_position_count"),
    ({"duplicate_intent_count": 1}, "duplicate_intent_count"),
    ({"unreserved_position_count": 1}, "unreserved_position_count"),
])
def test_reconciliation_failure_modes(changes, reason):
    state, reasons = status(**changes)
    assert state is EvidenceState.FAIL and reason in reasons
