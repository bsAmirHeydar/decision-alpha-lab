import copy,pytest
from saed_v4_hidden_evaluation_air_gap.contracts import parse_config,parse_candidate,parse_custody_manifest,parse_fixture
from saed_v4_hidden_evaluation_air_gap.errors import ContractError

def test_reference_config_parses(config): assert parse_config(config)["air_gap_policy"].maximum_evaluations==1
@pytest.mark.parametrize("section",["upstream_intake","air_gap_policy","air_gap_topology","custody_policy","evaluation_protocol","disclosure_policy"])
def test_unknown_top_level_section_field_rejected(config,section):
    bad=copy.deepcopy(config); bad[section]["unknown_field"]=1
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("field",["research_only","default_deny","one_shot_required","immutable_submission_required","sealed_evaluator_required","deterministic"])
def test_mandatory_air_gap_true(config,field):
    bad=copy.deepcopy(config); bad["air_gap_policy"][field]=False
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("field",["network_access","package_installation","interactive_debugging","shell_escape","raw_result_release","researcher_hidden_label_access","researcher_key_share_access"])
def test_forbidden_air_gap_capabilities(config,field):
    bad=copy.deepcopy(config); bad["air_gap_policy"][field]=True
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("field,value",[("maximum_evaluations",0),("maximum_evaluations",2),("maximum_round_trips",1),("fail_closed_action","continue")])
def test_one_shot_budget_exact(config,field,value):
    bad=copy.deepcopy(config); bad["air_gap_policy"][field]=value
    with pytest.raises(ContractError): parse_config(bad)
def test_topology_exact_zones(config):
    bad=copy.deepcopy(config); bad["air_gap_topology"]["zones"].pop()
    with pytest.raises(ContractError): parse_config(bad)
def test_research_zone_cannot_store_hidden(config):
    bad=copy.deepcopy(config); bad["air_gap_topology"]["zones"][0]["stores_plaintext_hidden_data"]=True
    with pytest.raises(ContractError): parse_config(bad)
def test_sealed_zone_has_no_network(config):
    bad=copy.deepcopy(config); [z for z in bad["air_gap_topology"]["zones"] if z["zone_id"]=="sealed_evaluator"][0]["network_access"]=True
    with pytest.raises(ContractError): parse_config(bad)
def test_raw_hidden_flow_denied(config):
    bad=copy.deepcopy(config); bad["air_gap_topology"]["flows"][0]["raw_hidden_data_allowed"]=True
    with pytest.raises(ContractError): parse_config(bad)
def test_protocol_metric_registry_complete(config):
    bad=copy.deepcopy(config); bad["evaluation_protocol"]["metric_specs"].pop()
    with pytest.raises(ContractError): parse_config(bad)
def test_protocol_no_adaptation(config):
    bad=copy.deepcopy(config); bad["evaluation_protocol"]["adaptive_changes_allowed"]=True
    with pytest.raises(ContractError): parse_config(bad)
def test_disclosure_allowlist_exact(config):
    bad=copy.deepcopy(config); bad["disclosure_policy"]["allowed_fields"].append("record_id")
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("field",["raw_rows_allowed","per_record_outputs_allowed","confusion_matrix_allowed","exact_thresholds_released"])
def test_disclosure_detail_denied(config,field):
    bad=copy.deepcopy(config); bad["disclosure_policy"][field]=True
    with pytest.raises(ContractError): parse_config(bad)
def test_candidate_parses(candidate): assert parse_candidate(candidate)["frozen"]
@pytest.mark.parametrize("field",["frozen"])
def test_candidate_must_be_frozen(candidate,field):
    bad=copy.deepcopy(candidate); bad[field]=False
    with pytest.raises(ContractError): parse_candidate(bad)
@pytest.mark.parametrize("field",["hidden_data_touched","adaptive_to_final_evaluation"])
def test_candidate_must_not_touch_final(candidate,field):
    bad=copy.deepcopy(candidate); bad[field]=True
    with pytest.raises(ContractError): parse_candidate(bad)
def test_candidate_network_dependencies_empty(candidate):
    bad=copy.deepcopy(candidate); bad["network_dependencies"]=["remote"]
    with pytest.raises(ContractError): parse_candidate(bad)
def test_candidate_hidden_training_role_rejected(candidate):
    bad=copy.deepcopy(candidate); bad["training_data_roles"].append("hidden_final")
    with pytest.raises(ContractError): parse_candidate(bad)
def test_custody_manifest_parses(config,manifest): assert parse_custody_manifest(manifest,parse_config(config)["custody_policy"])["threshold"]==2
def test_researcher_custody_access_denied(config,manifest):
    bad=copy.deepcopy(manifest); bad["researcher_read_access"]=True
    with pytest.raises(ContractError): parse_custody_manifest(bad,parse_config(config)["custody_policy"])
def test_custody_threshold_exact(config,manifest):
    bad=copy.deepcopy(manifest); bad["threshold"]=3
    with pytest.raises(ContractError): parse_custody_manifest(bad,parse_config(config)["custody_policy"])
def test_fixture_parses(config,manifest,fixture):
    m=parse_custody_manifest(manifest,parse_config(config)["custody_policy"]); assert len(parse_fixture(fixture,m)["records"])==48
def test_fixture_row_count_bound(config,manifest,fixture):
    bad=copy.deepcopy(fixture); bad["records"].pop(); m=parse_custody_manifest(manifest,parse_config(config)["custody_policy"])
    with pytest.raises(ContractError): parse_fixture(bad,m)
