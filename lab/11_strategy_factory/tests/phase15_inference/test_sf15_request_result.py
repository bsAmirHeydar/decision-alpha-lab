import math,pytest
from strategy_factory_inference.models import InferenceRequest,InferenceResult
from strategy_factory_inference.enums import InferenceStatus,RuntimeBackend

def request(order="order"):
 return InferenceRequest("","run","gen","frame","candidate","schema",order,1000,1000,(1.0,2.0),(False,False)).with_hash()
def test_request_identity_and_causality():
 r=request();r.validate(2);assert r.request_id.startswith("ireq_") and r.request_hash.startswith("ireqh_")
 with pytest.raises(ValueError):InferenceRequest("x","r","g","f","c","s","o",2,1,(1.0,),(False,)).validate(1)
def test_nonfinite_observed_feature_rejected():
 with pytest.raises(ValueError):InferenceRequest("x","r","g","f","c","s","o",1,1,(math.nan,),(False,)).validate(1)
def test_accepted_result_probability_range():
 x=InferenceResult("","req","m","1","rel","man",InferenceStatus.ACCEPTED,0.0,0.5,0,0.55,1,10,RuntimeBackend.PYTHON_REFERENCE).with_hash();x.validate()
