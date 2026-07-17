import copy,pytest
from saed_v4_anytime_valid_online_fdr.contracts import parse_config,parse_hypotheses,PROCEDURES
from saed_v4_anytime_valid_online_fdr.errors import ContractError

def test_config_parses(config): assert parse_config(config)["fdr_policy"].primary_procedure=="lord_plus_plus"
@pytest.mark.parametrize("section",["upstream_intake","fdr_policy","gamma_policy"])
def test_unknown_config_field_rejected(config,section):
    bad=copy.deepcopy(config); bad[section]["unknown_field"]=1
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("field",["anytime_valid_required","predictable_allocation_required","family_scoped","nonnegative_wealth_required","no_retroactive_mutation","rejection_requires_crossing","deterministic","research_only"])
def test_mandatory_fail_closed_controls(config,field):
    bad=copy.deepcopy(config); bad["fdr_policy"][field]=False
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("q",[0,-0.1,0.251,1.0])
def test_invalid_target_fdr(config,q):
    bad=copy.deepcopy(config); bad["fdr_policy"]["target_fdr"]=q
    with pytest.raises(ContractError): parse_config(bad)
@pytest.mark.parametrize("procedure",["bogus","","LORD"])
def test_unknown_procedure(config,procedure):
    bad=copy.deepcopy(config); bad["fdr_policy"]["primary_procedure"]=procedure
    with pytest.raises(ContractError): parse_config(bad)
def test_all_procedures_registered(): assert set(PROCEDURES)=={"alpha_spending","alpha_investing","lord_plus_plus","saffron","addis","e_lond"}
def test_gamma_sum_must_equal_one(config):
    bad=copy.deepcopy(config); bad["gamma_policy"]["weights"][0]+=0.01
    with pytest.raises(ContractError): parse_config(bad)
def test_gamma_nonincreasing(config):
    bad=copy.deepcopy(config); bad["gamma_policy"]["weights"][10]=bad["gamma_policy"]["weights"][0]
    s=sum(bad["gamma_policy"]["weights"]); bad["gamma_policy"]["weights"]=[x/s for x in bad["gamma_policy"]["weights"]]
    with pytest.raises(ContractError): parse_config(bad)
def test_family_weights_sum(config):
    bad=copy.deepcopy(config); bad["family_allocation"][0]["weight"]+=0.1
    with pytest.raises(ContractError): parse_config(bad)
def test_family_allocation_frozen(config):
    bad=copy.deepcopy(config); bad["family_allocation"][0]["frozen_before_first_test"]=False
    with pytest.raises(ContractError): parse_config(bad)
def test_stopping_rule_must_be_predictable(config):
    bad=copy.deepcopy(config); bad["stopping_rule_registry"][0]["predictable"]=False
    with pytest.raises(ContractError): parse_config(bad)
def test_stopping_rule_cannot_use_future(config):
    bad=copy.deepcopy(config); bad["stopping_rule_registry"][0]["uses_future_data"]=True
    with pytest.raises(ContractError): parse_config(bad)
def test_challenger_registry_complete(config):
    bad=copy.deepcopy(config); bad["challenger_registry"].pop()
    with pytest.raises(ContractError): parse_config(bad)
def test_hypotheses_parse(config,hypotheses):
    p=parse_config(config); assert len(parse_hypotheses(hypotheses,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]}))==36
@pytest.mark.parametrize("field",["hypothesis_id","sequence","family_id","decision_time","looks"])
def test_hypothesis_missing_field_rejected(config,hypotheses,field):
    bad=copy.deepcopy(hypotheses); del bad[0][field]; p=parse_config(config)
    with pytest.raises(ContractError): parse_hypotheses(bad,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]})
def test_hypothesis_order_contiguous(config,hypotheses):
    bad=copy.deepcopy(hypotheses); bad[1]["sequence"]=99; p=parse_config(config)
    with pytest.raises(ContractError): parse_hypotheses(bad,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]})
def test_anytime_p_running_min(config,hypotheses):
    bad=copy.deepcopy(hypotheses); bad[0]["looks"][1]["anytime_p_value"]=0.99; p=parse_config(config)
    with pytest.raises(ContractError): parse_hypotheses(bad,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]})
@pytest.mark.parametrize("value",[-1,1.1,float("inf")])
def test_p_value_range(config,hypotheses,value):
    bad=copy.deepcopy(hypotheses); bad[0]["looks"][0]["anytime_p_value"]=value; p=parse_config(config)
    with pytest.raises(ContractError): parse_hypotheses(bad,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]})
def test_e_value_nonnegative(config,hypotheses):
    bad=copy.deepcopy(hypotheses); bad[0]["looks"][0]["e_value"]=-1; p=parse_config(config)
    with pytest.raises(ContractError): parse_hypotheses(bad,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]})
