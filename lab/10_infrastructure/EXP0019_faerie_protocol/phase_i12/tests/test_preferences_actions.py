from fp_i12_operator import *
def test_toggle(config):
 p=default_preferences(config);r=apply_action(ActionRequest('A',OperatorAction.TOGGLE_PANEL),p);assert r.preferences.panel.state is PanelState.COLLAPSED
def test_set_mode(config):
 p=default_preferences(config);r=apply_action(ActionRequest('A',OperatorAction.SET_MODE,'AUDIT'),p);assert r.preferences.panel.mode is PanelMode.AUDIT
def test_export_request(config):assert apply_action(ActionRequest('A',OperatorAction.EXPORT_SNAPSHOT),default_preferences(config)).export_requested
def test_rebuild_request(config):assert apply_action(ActionRequest('A',OperatorAction.REQUEST_REBUILD),default_preferences(config)).rebuild_requested
def test_invalid_mode(config):assert apply_action(ActionRequest('A',OperatorAction.SET_MODE,'BAD'),default_preferences(config)).disposition is ActionDisposition.REJECTED
