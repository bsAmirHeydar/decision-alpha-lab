from fp_i12_operator import *
def test_restart_preserves_dedupe(snapshot,config):
 e=OperatorUXEngine(config);e.process(snapshot);cp=build_checkpoint(config,e.preferences,e.alerts.snapshot(),snapshot.computed_hash);e2=OperatorUXEngine(config,cp);o=e2.process(snapshot,140);assert all(a.disposition is not AlertDisposition.DELIVERED for a in o.alerts)
def test_restart_preserves_preferences(snapshot,config):
 e=OperatorUXEngine(config);e.action(ActionRequest('A',OperatorAction.SET_MODE,'AUDIT'));cp=build_checkpoint(config,e.preferences,e.alerts.snapshot(),snapshot.computed_hash);assert OperatorUXEngine(config,cp).preferences.panel.mode is PanelMode.AUDIT
