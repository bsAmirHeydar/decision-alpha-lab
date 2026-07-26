from __future__ import annotations
from src.engine.tooling.strategy_factory.lcm.lcm_13b.canonical import verify_embedded_digest
from src.engine.tooling.strategy_factory.lcm.lcm_13b.io import load_json

def test_reference_owner_approval_is_narrow(cutover_root):
    approval = load_json(cutover_root / "owner_approval_registry.json")
    assert approval["approval_state"] == "APPROVED_REFERENCE_SCOPE_ONLY"
    assert approval["approved_consumer_count"] == 613
    assert approval["production_runtime_approval"] is False
    assert approval["live_order_approval"] is False
    assert approval["capital_approval"] is False
    assert approval["source_deletion_approval"] is False
    assert verify_embedded_digest(approval, "approval_digest")

def test_handoff_only_allows_rollback_closure(cutover_root):
    handoff = load_json(cutover_root / "LCM13B_TO_LCM13C_HANDOFF.json")
    assert handoff["handoff_type"] == "LCM13B_TO_LCM13C"
    assert handoff["consumer_cutover_performed"] is True
    assert handoff["rollback_rehearsal_performed"] is False
    assert "RUN_REPRESENTATIVE_AND_HIGH_RISK_ROLLBACK_REHEARSALS" in handoff["allowed_next_actions"]
    assert "DELETE_LEGACY_SOURCE" in handoff["forbidden_actions"]
    assert "CUTOVER_BLOCKED_CONSUMER" in handoff["forbidden_actions"]
    assert verify_embedded_digest(handoff, "handoff_digest")
