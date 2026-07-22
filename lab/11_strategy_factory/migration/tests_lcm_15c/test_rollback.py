import json
def test_rollback(package_root):d=json.loads((package_root/'rollback_manifest.json').read_text());assert d['deleted_path_count']==0 and d['source_restore_required'] is False
