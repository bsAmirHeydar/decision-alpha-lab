import json
def test_ledger(package_root):d=json.loads((package_root/'deletion_ledger.json').read_text());assert d['deleted_path_count']==d['deletion_record_count']==0
