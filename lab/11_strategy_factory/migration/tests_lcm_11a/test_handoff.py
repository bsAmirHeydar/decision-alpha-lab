import json
def test_handoff_is_bounded(inventory_root):
    hand=json.loads((inventory_root/'LCM11A_TO_LCM11B_HANDOFF.json').read_text())
    assert hand['handoff_type']=='LCM11A_TO_LCM11B'
    assert hand['validation_status']=='PASS'
    assert hand['runtime_authority_created'] is False
    assert hand['live_order_authority_created'] is False
    assert hand['capital_authority_created'] is False
    assert hand['consumer_cutover_allowed'] is False
    assert 'IMPLEMENT_CANONICAL_VISUALIZERS' in hand['allowed_next_actions']
