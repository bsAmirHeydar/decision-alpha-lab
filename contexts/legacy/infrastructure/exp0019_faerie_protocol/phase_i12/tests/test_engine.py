from fp_i12_operator import *
def test_engine_output(snapshot,config):
 o=OperatorUXEngine(config).process(snapshot);assert o.panel.total_items==4 and len(o.alerts)>0
def test_engine_deterministic(snapshot,config):
 a=OperatorUXEngine(config).process(snapshot);b=OperatorUXEngine(config).process(snapshot);assert a.output_hash==b.output_hash
def test_filter_action_projection_only(snapshot,config):
 e=OperatorUXEngine(config);before=snapshot.computed_hash;e.action(ActionRequest('A',OperatorAction.FOCUS_SEMANTIC_ID,'SIG-1'));o=e.process(snapshot);assert o.snapshot_hash==before and o.panel.total_items==1
def test_manual_export(snapshot,config):
 e=OperatorUXEngine(config);e.action(ActionRequest('A',OperatorAction.EXPORT_SNAPSHOT));o=e.process(snapshot);assert len(o.exports)==2
def test_second_process_no_duplicate_alert(snapshot,config):
 e=OperatorUXEngine(config);e.process(snapshot);o=e.process(snapshot,131);assert all(a.disposition is not AlertDisposition.DELIVERED for a in o.alerts)
