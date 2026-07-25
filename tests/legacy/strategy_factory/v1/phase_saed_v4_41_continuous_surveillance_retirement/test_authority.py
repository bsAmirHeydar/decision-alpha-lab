def test_authority_fail_closed(output):
 a=output['authority'];assert a['may_submit_live_order'] is False;assert a['may_activate_capital'] is False;assert a['may_cross_tenant_action'] is False;assert a['may_reinstate_without_new_qualification'] is False
def test_release_no_authority(output):
 r=output['release'];assert r['live_order_submission_allowed'] is False;assert r['capital_activation_allowed'] is False;assert r['automatic_live_action_allowed'] is False;assert r['production_authorized'] is False
def test_no_side_effects(output):
 assert output['actions']['live_order_side_effects']==0;assert output['actions']['capital_delta']==0.0;assert output['retirement']['live_order_side_effects']==0;assert output['verification']['live_order_side_effects']==0
