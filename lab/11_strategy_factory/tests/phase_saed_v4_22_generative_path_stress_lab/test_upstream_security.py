import copy,pytest
from saed_v4_generative_path_stress_lab.upstream import validate_upstream
from saed_v4_generative_path_stress_lab.security import scan
from saed_v4_generative_path_stress_lab.errors import UpstreamError,AuthorityError

def test_upstream_valid(config,upstream):assert validate_upstream(config['upstream_intake'],upstream)['hash_verified']
@pytest.mark.parametrize('doc,key',[('robust_certificate','certificate_hash'),('scenario_set','scenario_set_hash'),('ambiguity_set','ambiguity_set_hash'),('budget','ledger_hash'),('handoff','handoff_hash')])
def test_upstream_hash_mismatch(config,upstream,doc,key):
    u=copy.deepcopy(upstream);u[doc][key]='bad'
    with pytest.raises(UpstreamError):validate_upstream(config['upstream_intake'],u)
@pytest.mark.parametrize('key',['api_key','secret','password','token','live_credential','broker_credential','protected_final_evidence','hidden_evaluation_label','live_order','order_ticket'])
def test_security_forbidden_keys(key):
    with pytest.raises(AuthorityError):scan({key:'x'})
