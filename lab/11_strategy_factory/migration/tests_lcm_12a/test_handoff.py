def test_handoff_boundary(load):
    h=load("LCM12A_TO_LCM12B_HANDOFF.json")
    assert h["handoff_type"]=="LCM12A_TO_LCM12B"
    assert h["runtime_authority_created"] is False
    assert h["live_order_authority_created"] is False
    assert h["capital_authority_created"] is False
    assert "DELETE_DOCUMENT" in h["forbidden_actions"]
