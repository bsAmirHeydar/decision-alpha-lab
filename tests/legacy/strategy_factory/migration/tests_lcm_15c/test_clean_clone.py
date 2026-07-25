import json
def test_clean_clone(package_root):d=json.loads((package_root/'clean_clone_verification.json').read_text());assert d['clean_clone_result']=='PASS' and d['source_manifest_digest']==d['clone_manifest_digest']
