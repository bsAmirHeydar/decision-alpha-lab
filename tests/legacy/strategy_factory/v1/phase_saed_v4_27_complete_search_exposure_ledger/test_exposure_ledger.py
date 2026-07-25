import copy, pytest
from saed_v4_complete_search_exposure_ledger import run
from saed_v4_complete_search_exposure_ledger.chain import verify_chain
from saed_v4_complete_search_exposure_ledger.errors import IntegrityError, BudgetExceededError

def test_exposure_complete(outputs): assert outputs["exposure_ledger"]["complete"]
def test_exposure_count(outputs): assert outputs["exposure_ledger"]["event_count"]==44
def test_exposure_chain(outputs): assert verify_chain(outputs["exposure_ledger"]["entries"],"exposure_ledger")["verified"]
@pytest.mark.parametrize("kind",["notebook_open","query_submitted","metric_read","chart_render","dashboard_open","agent_summary","example_inspection","row_export","narrative_generated","hypothesis_modified","manual_intervention"])
def test_exposure_type_present(outputs,kind): assert outputs["exposure_ledger"]["counts_by_type"][kind]>0
@pytest.mark.parametrize("field",["hidden_evaluation_queries","protected_evidence_exposures","runtime_compilations","order_submissions","online_policy_mutations","network_requests"])
def test_forbidden_counts_zero(outputs,field): assert outputs["exposure_ledger"][field]==0
def test_protected_role_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(exposures); bad[0]["data_role"]="protected_final"
    with pytest.raises(IntegrityError): run(config,upstream,manifests,trials,bad)
def test_hidden_role_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(exposures); bad[0]["data_role"]="hidden_evaluation"
    with pytest.raises(IntegrityError): run(config,upstream,manifests,trials,bad)
def test_unknown_actor_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(exposures); bad[0]["actor_id"]="unknown"
    with pytest.raises(IntegrityError): run(config,upstream,manifests,trials,bad)
def test_exposure_tamper_detected(outputs):
    bad=copy.deepcopy(outputs["exposure_ledger"]["entries"]); bad[-1]["purpose"]="tampered"
    with pytest.raises(IntegrityError): verify_chain(bad,"exposure_ledger")
def test_exposure_budget_rejected(config,upstream,manifests,trials,exposures):
    badc=copy.deepcopy(config); badc["query_budget"]["maximum_exposures"]=10
    with pytest.raises(BudgetExceededError): run(badc,upstream,manifests,trials,exposures)
