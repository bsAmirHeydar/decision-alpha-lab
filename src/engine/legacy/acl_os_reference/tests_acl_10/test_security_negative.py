import json, pytest
from src.engine.tooling.strategy_factory.acl_os.acl_10.canonical import with_digest
from src.engine.tooling.strategy_factory.acl_os.acl_10.errors import AuthorityError,PolicyError,PublicationError
from src.engine.tooling.strategy_factory.acl_os.acl_10.service import ACL10PromotionStateService

def test_capital_permit_rejected(acl09_root,permit,policy,tmp_path):
    bad={**permit,'capital_activation_allowed':True}; bad=with_digest({k:v for k,v in bad.items() if k!='permit_digest'},'permit_digest')
    with pytest.raises(AuthorityError): ACL10PromotionStateService().build(acl09_root,bad,policy,tmp_path/'o','2026-07-18T03:00:00Z')
def test_runtime_policy_rejected(acl09_root,permit,policy,tmp_path):
    bad={**policy,'runtime_generation_allowed':True}; bad=with_digest({k:v for k,v in bad.items() if k!='policy_digest'},'policy_digest')
    with pytest.raises(PolicyError): ACL10PromotionStateService().build(acl09_root,permit,bad,tmp_path/'o','2026-07-18T03:00:00Z')
def test_nonempty_destination_rejected(acl09_root,permit,policy,tmp_path):
    dest=tmp_path/'o'; dest.mkdir(); (dest/'x').write_text('x')
    with pytest.raises(PublicationError): ACL10PromotionStateService().build(acl09_root,permit,policy,dest,'2026-07-18T03:00:00Z')
def test_no_order_or_capital_true(reference):
    for p in reference.rglob('*.json'):
        d=json.loads(p.read_text())
        text=json.dumps(d)
        assert '"live_order_submission_allowed": true' not in text
        assert '"capital_activation_allowed": true' not in text
