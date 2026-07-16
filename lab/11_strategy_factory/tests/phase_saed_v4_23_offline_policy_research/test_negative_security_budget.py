import copy,pytest
from saed_v4_offline_policy_research.security import scan
from saed_v4_offline_policy_research.errors import AuthorityError,BudgetError,UpstreamError
from saed_v4_offline_policy_research.contracts import ResearchBudget
from saed_v4_offline_policy_research.budget import ResearchLedger
from saed_v4_offline_policy_research.upstream import verify
@pytest.mark.parametrize('key',['api_key','secret','password','token','live_credential','broker_credential','protected_final_evidence','hidden_evaluation_label','live_order','order_ticket','production_signing_key'])
def test_forbidden_security_key(key):
    with pytest.raises(AuthorityError):scan({key:'x'})
def test_budget_exhaustion(config):
    b=ResearchBudget.from_mapping(config['research_budget']);l=ResearchLedger(b)
    with pytest.raises(BudgetError):l.consume('training_trials',b.max_training_trials+1)
def test_upstream_mismatch(config,upstream):
    x=copy.deepcopy(upstream);x['V4_22_TO_V4_23_HANDOFF']['handoff_hash']='bad'
    with pytest.raises(UpstreamError):verify(config['upstream_intake'],x)
