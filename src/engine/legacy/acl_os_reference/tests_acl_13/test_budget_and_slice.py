import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_13.budget import validate_budget,usage_report
from src.engine.tooling.strategy_factory.acl_os.acl_13.slice import build_fast_slice
from src.engine.tooling.strategy_factory.acl_os.acl_13.errors import BudgetError
def test_budget_valid(budget,assessment_request): assert validate_budget(budget,assessment_request)['within_budget']
def test_one_hour_exact_budget_required(budget,assessment_request):
    b=copy.deepcopy(budget); b['wall_clock_budget_seconds']=7200
    with pytest.raises(BudgetError): validate_budget(b,assessment_request)
def test_observation_budget_denied(budget,assessment_request):
    b=copy.deepcopy(budget); b['max_observations']=1
    with pytest.raises(BudgetError): validate_budget(b,assessment_request)
def test_slice_deterministic(assessment_request): assert build_fast_slice(assessment_request)==build_fast_slice(assessment_request)
def test_slice_sorted(assessment_request):
    s=build_fast_slice(assessment_request); assert [x['observation_id'] for x in s['rows']]==sorted([x['observation_id'] for x in s['rows']])
def test_usage_no_network(budget,assessment_request): assert usage_report(budget,assessment_request,47)['network_calls']==0
