from fp_i12_operator import *
def test_jsonl_complete(snapshot,config):
 e=AuditExporter(config.instance_id,config.export);b=e.export(snapshot,ExportFormat.JSONL);assert b.appended_count==len(snapshot.items) and b.content.count('\n')==len(snapshot.items)
def test_csv_header(snapshot,config):
 b=AuditExporter(config.instance_id,config.export).export(snapshot,ExportFormat.CSV);assert b.content.startswith('record_id,instance_id')
def test_append_only_duplicate(snapshot,config):
 e=AuditExporter(config.instance_id,config.export);e.export(snapshot,ExportFormat.JSONL);b=e.export(snapshot,ExportFormat.JSONL);assert b.appended_count==0 and b.duplicate_count==len(snapshot.items)
def test_disabled(snapshot,config):
 e=AuditExporter(config.instance_id,ExportConfig(enabled=False));assert e.export(snapshot,ExportFormat.CSV).disposition is ExportDisposition.DISABLED
