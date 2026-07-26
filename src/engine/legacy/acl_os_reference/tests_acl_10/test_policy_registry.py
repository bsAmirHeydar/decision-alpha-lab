import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_10.canonical import with_digest
from src.engine.tooling.strategy_factory.acl_os.acl_10.errors import PolicyError
from src.engine.tooling.strategy_factory.acl_os.acl_10.promotion_policy import validate_promotion_policy
from src.engine.tooling.strategy_factory.acl_os.acl_10.state_registry import state_registry_snapshot,transition_registry_snapshot,prerequisite_registry_snapshot,validate_registries

def test_policy_valid(policy): assert validate_promotion_policy(policy)['evaluation_mode']=='EVALUATE_ONLY'
def test_unknown_must_block(policy):
    bad={**policy,'unknown_blocks_promotion':False}; bad=with_digest({k:v for k,v in bad.items() if k!='policy_digest'},'policy_digest')
    with pytest.raises(PolicyError): validate_promotion_policy(bad)
def test_self_approval_denied(policy):
    bad={**policy,'self_approval_allowed':True}; bad=with_digest({k:v for k,v in bad.items() if k!='policy_digest'},'policy_digest')
    with pytest.raises(PolicyError): validate_promotion_policy(bad)
def test_registries_validate(): validate_registries(state_registry_snapshot(),transition_registry_snapshot(),prerequisite_registry_snapshot())
def test_registry_counts(): assert len(state_registry_snapshot()['states'])==11 and len(transition_registry_snapshot()['transitions'])==7 and len(prerequisite_registry_snapshot()['prerequisites'])==21
def test_registry_drift_denied():
    s=state_registry_snapshot(); s['states']=s['states'][:-1]
    with pytest.raises(PolicyError): validate_registries(s,transition_registry_snapshot(),prerequisite_registry_snapshot())
