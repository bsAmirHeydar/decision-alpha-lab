import json
def test_post_reference(package_root):d=json.loads((package_root/'post_delete_reference_report.json').read_text());assert d['active_reference_count_to_deleted_paths']==0 and d['scan_target_count']==0
