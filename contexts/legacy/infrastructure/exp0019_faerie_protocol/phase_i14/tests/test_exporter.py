from fp_i14_diagnostic import *
def test_jsonl_append_dedup(tmp_path,runs):
    x=TraceExporter();r=runs[ProductKind.INDICATOR];a=x.export(r,tmp_path/'trace.jsonl',ExportFormat.JSONL);b=x.export(r,tmp_path/'trace.jsonl',ExportFormat.JSONL);assert a.appended_records==18 and b.duplicate_records==18 and len((tmp_path/'trace.jsonl').read_text().splitlines())==18
def test_csv_header_once(tmp_path,runs):
    x=TraceExporter();r=runs[ProductKind.INDICATOR];x.export(r,tmp_path/'trace.csv',ExportFormat.CSV);x.export(r,tmp_path/'trace.csv',ExportFormat.CSV);assert len((tmp_path/'trace.csv').read_text().splitlines())==19
def test_both_formats(tmp_path,runs):
    x=TraceExporter();x.export(runs[ProductKind.INDICATOR],tmp_path/'trace',ExportFormat.BOTH);assert (tmp_path/'trace.jsonl').exists() and (tmp_path/'trace.csv').exists()
