from tools.strategy_factory.lcm.lcm_12b.io import load_json
def test_handoff_only_allows_dual_run_next(reconciliation_root):
    handoff=load_json(reconciliation_root/"LCM12B_TO_LCM13A_HANDOFF.json")
    assert handoff["handoff_type"]=="LCM12B_TO_LCM13A"
    assert "BUILD_DUAL_RUN_HARNESS" in handoff["allowed_next_actions"]
    assert "PRODUCTION_CONSUMER_SWITCH" in handoff["forbidden_actions"]
    assert not handoff["runtime_authority_created"] and not handoff["live_order_authority_created"] and not handoff["capital_authority_created"]
