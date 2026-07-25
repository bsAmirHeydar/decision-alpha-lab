def test_handoff_is_reference_only_and_exact(dual_root):
    import json
    handoff = json.loads((dual_root / "LCM13A_TO_LCM13B_HANDOFF.json").read_text(encoding="utf-8"))
    assert handoff["handoff_type"] == "LCM13A_TO_LCM13B"
    assert handoff["consumer_counts"] == {
        "total": 1419,
        "eligible_for_wave_planning": 613,
        "blocked_remain_legacy": 806,
    }
    assert handoff["consumer_cutover_performed"] is False
    assert handoff["runtime_authority_created"] is False
    assert handoff["live_order_authority_created"] is False
    assert handoff["capital_authority_created"] is False
