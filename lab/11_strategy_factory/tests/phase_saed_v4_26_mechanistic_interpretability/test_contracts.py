from __future__ import annotations
import copy, pytest
from saed_v4_mechanistic_interpretability.contracts import parse_config
from saed_v4_mechanistic_interpretability.errors import ContractError

def test_full_config_parses(config): assert len(parse_config(config))==10
@pytest.mark.parametrize("section",["upstream_intake","mechanism_dataset_contract","attribution_contract","pathway_contract","concept_probe_contract","causal_trace_contract","counterfactual_contract","sparse_dictionary_contract","faithfulness_contract","research_budget"])
def test_unknown_fields_rejected(config,section):
    mutated=copy.deepcopy(config); mutated[section]["unknown_field"]=1
    with pytest.raises(ContractError): parse_config(mutated)
@pytest.mark.parametrize("section",["upstream_intake","mechanism_dataset_contract","attribution_contract","pathway_contract","concept_probe_contract","causal_trace_contract","counterfactual_contract","sparse_dictionary_contract","faithfulness_contract","research_budget"])
def test_missing_fields_rejected(config,section):
    mutated=copy.deepcopy(config); mutated[section].pop(next(iter(mutated[section])))
    with pytest.raises(ContractError): parse_config(mutated)
