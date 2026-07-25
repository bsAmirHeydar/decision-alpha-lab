import copy,pytest
from saed_v4_immutable_runtime_mql5_parity import run_reference
from saed_v4_immutable_runtime_mql5_parity.errors import SAEDV438Error
M=[
("upstream_unknown",lambda f:f["upstream"][0].__setitem__("unknown",1)),("upstream_prod",lambda f:f["upstream"][0].__setitem__("production_authorized",True)),("upstream_phase",lambda f:f["upstream"][0].__setitem__("phase","BAD")),
("constitution_mutable",lambda f:f["constitution"].__setitem__("immutable_bundle_required",False)),("constitution_order",lambda f:f["constitution"].__setitem__("automatic_order_submission_allowed",True)),("constitution_prod",lambda f:f["constitution"].__setitem__("production_authorization_allowed",True)),
("feature_unknown",lambda f:f["feature_abi"].__setitem__("x",1)),("feature_dup",lambda f:f["feature_abi"]["fields"][1].__setitem__("field_id",f["feature_abi"]["fields"][0]["field_id"])),("feature_ordinal",lambda f:f["feature_abi"]["fields"][1].__setitem__("ordinal",9)),("feature_bounds",lambda f:f["feature_abi"]["fields"][0].__setitem__("minimum",2)),
("model_unknown_feature",lambda f:f["model"]["features"].__setitem__(0,"bad_feature")),("model_weights",lambda f:f["model"]["weights"].pop()),("model_type",lambda f:f["model"].__setitem__("model_type","NEURAL")),
("policy_unknown_op",lambda f:f["policy_graph"]["nodes"][0].__setitem__("op","EXECUTE")),("policy_cycle",lambda f:f["policy_graph"]["nodes"][0]["inputs"].append(f["policy_graph"]["nodes"][-1]["node_id"])),("policy_ordinal",lambda f:f["policy_graph"]["nodes"][1].__setitem__("ordinal",8)),("policy_feature",lambda f:f["policy_graph"]["nodes"][0]["params"].__setitem__("name","unknown")),
("numeric_mode",lambda f:f["numeric_profile"].__setitem__("float_mode","FLOAT32")),("numeric_nan",lambda f:f["numeric_profile"].__setitem__("nan_policy","ALLOW")),("numeric_divzero",lambda f:f["numeric_profile"].__setitem__("division_zero_policy","ZERO")),
("clock_tz",lambda f:f["clock_profile"].__setitem__("timezone","America/New_York")),("clock_dst",lambda f:f["clock_profile"].__setitem__("dst_policy","LOCAL")),("clock_bar",lambda f:f["clock_profile"].__setitem__("bar_close_only",False)),
("compiler_network",lambda f:f["compiler_profile"].__setitem__("network_access",True)),("compiler_env",lambda f:f["compiler_profile"].__setitem__("environment_variables_allowed",True)),("compiler_time",lambda f:f["compiler_profile"].__setitem__("build_timestamp_policy","NOW")),
("future_vector",lambda f:f["parity_vectors"][0].__setitem__("known_time","2099-01-01T00:00:00Z")),("dup_vector",lambda f:f["parity_vectors"][1].__setitem__("vector_id",f["parity_vectors"][0]["vector_id"])),("vector_unknown",lambda f:f["parity_vectors"][0].__setitem__("unknown",1)),
("external_missing",lambda f:f["external_evidence"].pop()),("external_fake_pass",lambda f:[x.update({"status":"PASSED","actual_external_evidence":False}) for x in f["external_evidence"] if x["evidence_type"]=="METAEDITOR_COMPILE"]),("external_unknown",lambda f:f["external_evidence"][0].__setitem__("unknown",1)),
("review_duplicate",lambda f:f["reviews"][1].__setitem__("role",f["reviews"][0]["role"])),("review_reject",lambda f:f["reviews"][0].__setitem__("decision","YES")),("review_independent",lambda f:f["reviews"][0].__setitem__("independent",False)),
]
@pytest.mark.parametrize("name,mut",M,ids=[x[0] for x in M])
def test_mutation_fails_closed(fixture,name,mut):
 f=copy.deepcopy(fixture); mut(f)
 with pytest.raises((SAEDV438Error,ValueError,KeyError,TypeError)):run_reference(f)
