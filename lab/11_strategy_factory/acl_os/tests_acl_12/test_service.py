import json,pytest
from tools.strategy_factory.acl_os.acl_12.service import ACL12SecurityHardeningService
from tools.strategy_factory.acl_os.acl_12.verify import verify_output
from tools.strategy_factory.acl_os.acl_12.errors import PublicationError
def test_build_service(ACL11,permit,tmp_path):
    out=tmp_path/'out'; r=ACL12SecurityHardeningService().build(ACL11,permit,out); assert r['control_count']==33 and verify_output(out)['passed']
def test_reference_output_verifies(ACL12): assert verify_output(ACL12)['passed']
def test_deterministic_replay(ACL11,permit,tmp_path):
    a=tmp_path/'a'; b=tmp_path/'b'; s=ACL12SecurityHardeningService(); ra=s.build(ACL11,permit,a); rb=s.build(ACL11,permit,b); assert ra['handoff_digest']==rb['handoff_digest']
def test_nonempty_destination_denied(ACL11,permit,tmp_path):
    out=tmp_path/'out'; out.mkdir(); (out/'x').write_text('x')
    with pytest.raises(PublicationError): ACL12SecurityHardeningService().build(ACL11,permit,out)
def test_handoff_contract(ACL12):
    h=json.loads((ACL12/'handoff/acl13_handoff.json').read_text()); assert h['handoff_type']=='ACL12_TO_ACL13' and not h['production_security_ready']
