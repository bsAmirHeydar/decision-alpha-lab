from fp_i12_operator import *
def test_alert_state_isolated(config):
 a=AlertRouter('I1',config.alerts);b=AlertRouter('I2',config.alerts);c=AlertCandidate('S',AlertType.DATA_READY,100,AlertSeverity.INFO,'t','m',False,sha256('x'));a.route(c,100);assert not b.snapshot().delivered_ids
def test_export_state_isolated(snapshot,config):
 a=AuditExporter('I1',config.export);b=AuditExporter('I2',config.export);a.export(snapshot,ExportFormat.JSONL);assert b.export(snapshot,ExportFormat.JSONL).appended_count==len(snapshot.items)
