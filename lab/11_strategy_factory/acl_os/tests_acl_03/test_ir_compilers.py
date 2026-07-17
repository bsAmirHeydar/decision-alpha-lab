import copy,pytest
from tools.strategy_factory.acl_os.acl_03.detector_ir import compile_detector_ir
from tools.strategy_factory.acl_os.acl_03.occurrence_ir import compile_occurrence_ir,build_occurrence_id
from tools.strategy_factory.acl_os.acl_03.known_time_ir import compile_known_time_ir
from tools.strategy_factory.acl_os.acl_03.feature_binding_ir import compile_feature_binding_ir

def test_detector_is_deterministic(package): assert compile_detector_ir(package)[0]==compile_detector_ir(package)[0]
def test_detector_has_no_executable_code(package):
    ir,f=compile_detector_ir(package);assert not f;assert ir["generated_code_allowed"] is False;assert ir["execution_model"]=="DECLARATIVE_EVENT_GUARD_IR"
def test_transition_ids_unique(package):
    ir,_=compile_detector_ir(package);ids=[x["transition_id"] for x in ir["transitions"]];assert len(ids)==len(set(ids))
@pytest.mark.parametrize("token",["eval(","exec(","OrderSend(","CTrade","subprocess","socket.","requests.","open("])
def test_forbidden_guard_tokens_block(package,token):
    p=copy.deepcopy(package);p["state_machine"]["transitions"][0]["guard"]+=f" {token}";_,f=compile_detector_ir(p);assert "ACL03_FORBIDDEN_GUARD_TOKEN" in {x["code"] for x in f}
def test_occurrence_identity(package):
    ir,f=compile_occurrence_ir(package);assert not f;a=build_occurrence_id(ir,{"context_id":"CTX_REFERENCE_ALPHA","context_version":"0.1.0","anchor_time":"t","direction":"LONG","subject_key":"x"});b=build_occurrence_id(ir,{"context_id":"CTX_REFERENCE_ALPHA","context_version":"0.1.0","anchor_time":"t","direction":"LONG","subject_key":"x"});assert a==b
@pytest.mark.parametrize("field",["context_id","context_version","anchor_time","direction","subject_key"])
def test_occurrence_missing_required_field(package,field):
    p=copy.deepcopy(package);p["occurrence"]["identity_fields"].remove(field);_,f=compile_occurrence_ir(p);assert "ACL03_OCCURRENCE_IDENTITY_INCOMPLETE" in {x["code"] for x in f}
@pytest.mark.parametrize("relation",["event_time<=observation_time","observation_time<=known_time","known_time<=decision_time","decision_time<=maturity_time","maturity_time<=correction_time"])
def test_clock_relation_required(package,relation):
    p=copy.deepcopy(package);p["causal_clock"]["required_order"].remove(relation);_,f=compile_known_time_ir(p);assert "ACL03_CLOCK_ORDER_MISSING" in {x["code"] for x in f}
def test_feature_order_frozen(package):
    ir,f=compile_feature_binding_ir(package);assert not f;assert ir["feature_order_frozen"] is True
