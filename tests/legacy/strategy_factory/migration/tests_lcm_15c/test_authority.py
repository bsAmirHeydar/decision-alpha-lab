import json
def test_authority(package_root):d=json.loads((package_root/'LCM15C_TO_LCM16A_HANDOFF.json').read_text());assert not any(d[k] for k in ['runtime_authority_created','live_order_authority_created','capital_authority_created','deletion_authority_created'])
