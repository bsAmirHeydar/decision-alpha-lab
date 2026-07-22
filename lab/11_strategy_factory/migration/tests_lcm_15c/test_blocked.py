import json
def test_blocked(package_root):d=json.loads((package_root/'blocked_deletion_registry.json').read_text());assert d['blocked_count']==2168 and d['approved_count']==0
