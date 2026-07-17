from __future__ import annotations
import copy, pytest
from saed_v4_mechanistic_interpretability.budget import ResearchLedger
from saed_v4_mechanistic_interpretability.contracts import parse_config
from saed_v4_mechanistic_interpretability.dataset import validate
from saed_v4_mechanistic_interpretability.errors import ContractError, KnownTimeError

def parts(config):
 p=parse_config(config); return p["mechanism_dataset_contract"],ResearchLedger(p["research_budget"])
def test_valid_dataset(config,records):
 c,l=parts(config); s=validate(records,c,l); assert s["record_count"]==40 and s["known_time_verified"]
@pytest.mark.parametrize("field,value,error",[("future_suffix_accessed",True,KnownTimeError),("protected_evidence_accessed",True,KnownTimeError),("immutable_model",False,ContractError),("known_time","2035-01-01T00:00:00Z",KnownTimeError)])
def test_safety_mutations(config,records,field,value,error):
 c,l=parts(config); m=copy.deepcopy(records); m[0][field]=value
 with pytest.raises(error): validate(m,c,l)
@pytest.mark.parametrize("index",range(6))
def test_feature_dimension_mutations(config,records,index):
 c,l=parts(config); m=copy.deepcopy(records); m[index]["feature_values"].pop()
 with pytest.raises(ContractError): validate(m,c,l)
