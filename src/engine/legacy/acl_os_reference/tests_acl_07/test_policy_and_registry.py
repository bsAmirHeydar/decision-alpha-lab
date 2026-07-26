import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_07.validation_policy import validate_policy
from src.engine.tooling.strategy_factory.acl_os.acl_07.gate_registry import registry_snapshot,validate_registry
from src.engine.tooling.strategy_factory.acl_os.acl_07.errors import PolicyError

def test_policy_accepts(policy): assert validate_policy(policy)['policy_id']
def test_policy_denies_promotion(policy): assert validate_policy(policy)['promotion_authority_granted'] is False
def test_policy_rejects_bad_coverage(policy):
 bad=copy.deepcopy(policy); bad['thresholds']['minimum_coverage']=2
 with pytest.raises(PolicyError): validate_policy(bad)
def test_registry_closed(): assert validate_registry(registry_snapshot())['closed_world'] is True
def test_registry_has_15_gates(): assert len(registry_snapshot()['entries'])==15
def test_registry_rejects_mutation():
 bad=registry_snapshot(); bad['entries'][0]['gate_id']='ALTERED'
 with pytest.raises(PolicyError): validate_registry(bad)
