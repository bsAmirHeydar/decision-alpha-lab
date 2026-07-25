def test_handoff_allows_only_bounded_next_actions(load):
    handoff = load("LCM16A_TO_LCM16B_HANDOFF.json")
    assert handoff["closure_decision"] == "BLOCKED"
    assert handoff["allowed_next_actions"] == [
        "LCM16B_RECOVERY_DRILL_PREPARATION",
        "CAPTURE_EXTERNAL_METAEDITOR_AND_STRATEGY_TESTER_EVIDENCE",
        "RESOLVE_EXTERNAL_CONSUMER_REACHABILITY",
    ]
    assert "DECLARE_LEGACY_MIGRATION_PROGRAM_CLOSED" in handoff["forbidden_actions"]
    for key in (
        "runtime_authority_created", "live_order_authority_created",
        "capital_authority_created", "deletion_authority_created",
    ):
        assert handoff[key] is False
