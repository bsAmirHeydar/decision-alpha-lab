from src.engine.tooling.strategy_factory.lcm.lcm_16b.io import load_json


def test_all_authorities_false(package_root):
    authority = load_json(package_root / "authority_final_state.json")
    keys = [key for key in authority if key.endswith("authority")]
    assert keys
    assert all(authority[key] is False for key in keys)


def test_deletion_state_is_zero(package_root):
    deletion = load_json(package_root / "deletion_final_state.json")
    assert deletion["approved_deletion_count"] == 0
    assert deletion["executed_deletion_count"] == 0
    assert deletion["wildcard_delete_used"] is False


def test_continuity_not_activated(package_root):
    handoff = load_json(package_root / "post_program_continuity_handoff.json")
    assert handoff["handoff_state"] == "NOT_ACTIVATED_PROGRAM_OPEN_BLOCKED"
    assert "REEVALUATE_LCM16B_PROGRAM_CLOSURE" in handoff["allowed_next_actions"]


def test_acceptance_claim_is_bounded(package_root):
    report = load_json(package_root / "reports/acceptance_report.json")
    assert report["phase_implementation_status"] == "PASS"
    assert report["program_closure_decision"] == "BLOCKED"
