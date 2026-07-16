import copy,pytest
from saed_v4_robust_optimization_regret.upstream import validate_upstream
from saed_v4_robust_optimization_regret.security import scan
from saed_v4_robust_optimization_regret.errors import UpstreamError,AuthorityError

def test_upstream_verified(config,upstream):assert validate_upstream(config['upstream_intake'],upstream['certificate'],upstream['registry'],upstream['exposure'],upstream['handoff'])['hash_verified']
@pytest.mark.parametrize('field',['selection_certificate_hash','selection_registry_hash','exposure_ledger_hash'])
def test_hash_mismatch_rejected(config,upstream,field):
    x=copy.deepcopy(config['upstream_intake']);x[field]='0'*64
    with pytest.raises(UpstreamError):validate_upstream(x,upstream['certificate'],upstream['registry'],upstream['exposure'],upstream['handoff'])
@pytest.mark.parametrize('key',['api_key','secret','password','token','live_credential','broker_credential','protected_final_evidence','hidden_evaluation_label'])
def test_security_forbidden_keys(key):
    with pytest.raises(AuthorityError):scan({'nested':{key:'x'}})
def test_security_clean(config):assert scan(config)
