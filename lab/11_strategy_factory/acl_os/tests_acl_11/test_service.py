from tools.strategy_factory.acl_os.acl_11.service import ACL11RuntimeCustodyService
from tools.strategy_factory.acl_os.acl_11.verify import verify_output
def test_build_and_verify(tmp_path,acl10,permit):
    out=tmp_path/'out'; result=ACL11RuntimeCustodyService().build(acl10,permit,out); assert result['runtime_candidate_count']==0; assert verify_output(out)['passed']
def test_atomic_destination_guard(tmp_path,acl10,permit):
    from tools.strategy_factory.acl_os.acl_11.errors import PublicationError
    out=tmp_path/'out'; out.mkdir(); (out/'x').write_text('x')
    try: ACL11RuntimeCustodyService().build(acl10,permit,out)
    except PublicationError: pass
    else: raise AssertionError('non-empty destination accepted')
def test_replay_is_deterministic(tmp_path,acl10,permit):
    s=ACL11RuntimeCustodyService(); a=tmp_path/'a'; b=tmp_path/'b'; s.build(acl10,permit,a); s.build(acl10,permit,b)
    import json
    da=json.loads((a/'run/runtime_custody_run.json').read_text()); db=json.loads((b/'run/runtime_custody_run.json').read_text()); assert da['runtime_custody_run_digest']==db['runtime_custody_run_digest']
