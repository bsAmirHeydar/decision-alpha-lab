from tools.strategy_factory.acl_os.acl_11.service import ACL11RuntimeCustodyService
import json
def test_acl12_handoff_denies_runtime(tmp_path,acl10,permit):
    out=tmp_path/'o'; ACL11RuntimeCustodyService().build(acl10,permit,out); h=json.loads((out/'handoff/acl12_handoff.json').read_text()); assert h['handoff_type']=='ACL11_TO_ACL12' and h['runtime_generation_allowed'] is False
def test_acl12_required_actions(tmp_path,acl10,permit):
    out=tmp_path/'o'; ACL11RuntimeCustodyService().build(acl10,permit,out); h=json.loads((out/'handoff/acl12_handoff.json').read_text()); assert 'HARDEN_SECURITY_BOUNDARIES' in h['required_acl12_actions']
