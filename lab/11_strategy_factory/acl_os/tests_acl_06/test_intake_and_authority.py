import copy,pytest
from tools.strategy_factory.acl_os.acl_06.canonical import digest_object
def redigest(d,field): d[field]=digest_object({k:v for k,v in d.items() if k!=field}); return d
def test_wrong_authority_action_denied(build,inputs):
    p=copy.deepcopy(inputs['authority_permit']); p['action']='ACL06_FORBIDDEN'; redigest(p,'permit_digest')
    with pytest.raises(Exception): build(force=True,authority_permit=p)
def test_network_authority_denied(build,inputs):
    p=copy.deepcopy(inputs['authority_permit']); p['network_access_allowed']=True; redigest(p,'permit_digest')
    with pytest.raises(Exception): build(force=True,authority_permit=p)
def test_tampered_request_denied(build,inputs):
    q=copy.deepcopy(inputs['run_request']); q['purpose']='tampered without digest update'
    with pytest.raises(Exception): build(force=True,run_request=q)
def test_nonempty_output_denied(build,tmp_path):
    p=tmp_path/'out'; p.mkdir(); (p/'x').write_text('x')
    with pytest.raises(Exception): build(force=True)
