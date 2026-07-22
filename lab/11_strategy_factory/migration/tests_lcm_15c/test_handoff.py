import json
def test_handoff(package_root):d=json.loads((package_root/'LCM15C_TO_LCM16A_HANDOFF.json').read_text());assert d['allowed_next_actions']==['LCM16A_FULL_SYSTEM_AUDIT'] and d['deleted_path_count']==0
