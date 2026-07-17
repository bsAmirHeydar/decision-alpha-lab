import copy,pytest
from saed_v4_immutable_runtime_mql5_parity.runtime import evaluate,validate_features
from saed_v4_immutable_runtime_mql5_parity.parity import mql5_reference_emulator
from saed_v4_immutable_runtime_mql5_parity.errors import RuntimeError438

def _parts(output):
 a=next(x for x in output["abi_registry"]["abis"] if x["kind"]=="FEATURE")
 return output["policy_graph"],output["model"],a,output["initial_state"]
@pytest.mark.parametrize("idx",range(48))
def test_each_vector_matches_expected(output,idx):
 g,m,a,s=_parts(output); v=output["parity_vectors"]["vectors"][idx]; d=evaluate(g,m,v["features"],a,s)
 assert d["decision"]==v["expected_decision"]; assert d["treatment_id"]==v["expected_treatment_id"]; assert d["confidence"]==v["expected_confidence"]; assert d["net_edge_bps"]==v["expected_net_edge_bps"]; assert d["size_fraction"]==v["expected_size_fraction"]
@pytest.mark.parametrize("idx",range(48))
def test_each_vector_python_emulator_exact(output,idx):
 g,m,a,s=_parts(output); v=output["parity_vectors"]["vectors"][idx]; assert evaluate(g,m,v["features"],a,s)==mql5_reference_emulator(g,m,v["features"],a,s)
def test_unknown_feature_fails(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][0]["features"]); f["unknown"]=1
 with pytest.raises(RuntimeError438):evaluate(g,m,f,a,s)
def test_missing_feature_fails(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][0]["features"]); f.pop("ood_score")
 with pytest.raises(RuntimeError438):evaluate(g,m,f,a,s)
def test_nan_fails(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][0]["features"]); f["ood_score"]=float("nan")
 with pytest.raises(RuntimeError438):evaluate(g,m,f,a,s)
def test_inf_fails(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][0]["features"]); f["ood_score"]=float("inf")
 with pytest.raises(RuntimeError438):evaluate(g,m,f,a,s)
def test_ood_abstains(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][1]["features"]); f["ood_score"]=.21; assert evaluate(g,m,f,a,s)["decision"]=="ABSTAIN"
def test_risk_abstains(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][1]["features"]); f["portfolio_risk"]=.81; assert evaluate(g,m,f,a,s)["decision"]=="ABSTAIN"
def test_edge_abstains(output):
 g,m,a,s=_parts(output); f=copy.deepcopy(output["parity_vectors"]["vectors"][1]["features"]); f["expected_edge_bps"]=f["expected_cost_bps"]+2.99; assert evaluate(g,m,f,a,s)["decision"]=="ABSTAIN"
