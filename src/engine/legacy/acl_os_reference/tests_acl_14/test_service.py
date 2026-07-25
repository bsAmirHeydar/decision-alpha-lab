from tools.strategy_factory.acl_os.acl_14.service import ACL14FirstRealContextPilotService
from tools.strategy_factory.acl_os.acl_14.verify import verify_output

def test_build_and_verify(tmp_path,acl13_root,permit,pilot_request,policy):
    out=tmp_path/'out'
    result=ACL14FirstRealContextPilotService().build(acl13_root,permit,pilot_request,policy,out)
    assert result['passed']
    assert verify_output(out)['passed']

def test_deterministic_replay(tmp_path,acl13_root,permit,pilot_request,policy):
    first=tmp_path/'first'; second=tmp_path/'second'
    service=ACL14FirstRealContextPilotService()
    r1=service.build(acl13_root,permit,pilot_request,policy,first)
    r2=service.build(acl13_root,permit,pilot_request,policy,second)
    assert r1['pilot_run_id']==r2['pilot_run_id']
    assert r1['handoff_digest']==r2['handoff_digest']

def test_destination_conflict(tmp_path,acl13_root,permit,pilot_request,policy):
    out=tmp_path/'out'; out.mkdir(); (out/'x').write_text('x')
    import pytest
    with pytest.raises(Exception):
        ACL14FirstRealContextPilotService().build(acl13_root,permit,pilot_request,policy,out)

def test_reference_output_state(tmp_path,acl13_root,permit,pilot_request,policy):
    out=tmp_path/'out'
    ACL14FirstRealContextPilotService().build(acl13_root,permit,pilot_request,policy,out)
    assert verify_output(out)['state']=='PILOT_CONTRACT_AUTHORED_REAL_EVIDENCE_REQUIRED'
