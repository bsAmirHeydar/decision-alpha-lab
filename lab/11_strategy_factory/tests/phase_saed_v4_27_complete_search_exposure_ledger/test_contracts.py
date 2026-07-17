import copy, pytest
from saed_v4_complete_search_exposure_ledger.contracts import parse_config, parse_manifests, TRIAL_STATES, DATA_ROLES, EXPOSURE_TYPES
from saed_v4_complete_search_exposure_ledger.errors import ContractError

def test_config_parses(config): assert parse_config(config)["ledger_policy"].append_only
@pytest.mark.parametrize("section",["upstream_intake","ledger_policy","query_budget"])
def test_unknown_config_fields_rejected(config,section):
    bad=copy.deepcopy(config); bad[section]["unknown_field"]=1
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("field",["append_only","hash_chain_required","actor_identity_required","data_role_required","known_time_required","complete_failure_accounting","duplicate_accounting","retry_accounting","orphan_runs_forbidden","protected_exposure_forbidden","deterministic"])
def test_required_policy_controls_fail_closed(config,field):
    bad=copy.deepcopy(config); bad["ledger_policy"][field]=False
    with pytest.raises(ContractError): parse_config(bad)
def test_hidden_budget_must_be_zero(config):
    bad=copy.deepcopy(config); bad["query_budget"]["maximum_hidden_evaluation_queries"]=1
    with pytest.raises(ContractError): parse_config(bad)
def test_protected_budget_must_be_zero(config):
    bad=copy.deepcopy(config); bad["query_budget"]["maximum_protected_exposures"]=1
    with pytest.raises(ContractError): parse_config(bad)
def test_manifest_parses(manifests): assert len(parse_manifests(manifests))==6
def test_manifest_unknown_rejected(manifests):
    bad=copy.deepcopy(manifests); bad[0]["x"]=1
    with pytest.raises(ContractError): parse_manifests(bad)
def test_registry_constants_complete():
    assert len(TRIAL_STATES)==12 and len(DATA_ROLES)==8 and len(EXPOSURE_TYPES)==11
