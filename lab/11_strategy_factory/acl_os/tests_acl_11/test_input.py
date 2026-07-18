import copy,pytest
from tools.strategy_factory.acl_os.acl_11.handoff_input import load_acl10_bundle
from tools.strategy_factory.acl_os.acl_11.errors import IntegrityError
def test_acl10_bundle_loads(acl10):
    b=load_acl10_bundle(acl10); assert b['runtime']['runtime_candidate_count']==0
def test_binding_is_content_addressed(acl10):
    b=load_acl10_bundle(acl10); assert b['binding']['binding_digest'].startswith('sha256:')
def test_upstream_authority_remains_denied(acl10):
    b=load_acl10_bundle(acl10); assert b['handoff']['runtime_generation_allowed'] is False
def test_upstream_decisions_are_non_promotional(acl10):
    b=load_acl10_bundle(acl10); assert b['decisions']['promotion_review_eligible_count']==0
