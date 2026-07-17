import copy,pytest
from saed_v4_formal_verification_safety_case.model import compile_model
from saed_v4_formal_verification_safety_case.properties import freeze_temporal
from saed_v4_formal_verification_safety_case.assurance import build
from saed_v4_formal_verification_safety_case.upstream import verify_upstream
from saed_v4_formal_verification_safety_case.errors import ContractError,ModelError,VerificationError,SafetyCaseError

def test_model_unknown_field_rejected(clone): clone["formal_model"]["unknown"]=1; pytest.raises(ContractError,compile_model,clone["formal_model"])
def test_model_wrong_phase_rejected(clone): clone["formal_model"]["phase"]="X"; pytest.raises(ModelError,compile_model,clone["formal_model"])
def test_model_authority_transition_rejected(clone): clone["formal_model"]["transitions"][0]["authority_free"]=False; pytest.raises(ModelError,compile_model,clone["formal_model"])
def test_model_unknown_guard_name_rejected(clone): clone["formal_model"]["transitions"][0]["guard"]="future_price > 0"; pytest.raises(VerificationError,compile_model,clone["formal_model"])
def test_model_call_expression_rejected(clone): clone["formal_model"]["transitions"][0]["guard"]="open('x')"; pytest.raises(VerificationError,compile_model,clone["formal_model"])
def test_model_duplicate_transition_rejected(clone): clone["formal_model"]["transitions"][1]["transition_id"]="T-001"; pytest.raises(ContractError,compile_model,clone["formal_model"])
def test_model_duplicate_action_rejected(clone): clone["formal_model"]["transitions"][1]["action"]="ingest_verified_upstream"; pytest.raises(ModelError,compile_model,clone["formal_model"])
def test_model_invalid_initial_domain_rejected(clone): clone["formal_model"]["initial_state"]["stage"]="UNKNOWN"; pytest.raises(ModelError,compile_model,clone["formal_model"])
def test_temporal_unknown_kind_rejected(clone): clone["temporal_properties"][0]["kind"]="unbounded_ltl"; pytest.raises(VerificationError,freeze_temporal,clone["temporal_properties"])
def test_upstream_authority_rejected(clone): clone["upstream_documents"]["handoff"]["authority"]["execution"]=True; pytest.raises(ContractError,verify_upstream,clone["upstream_documents"])
def test_upstream_phase_rejected(clone): clone["upstream_documents"]["handoff"]["next_phase"]="SAED_V4_32"; pytest.raises(ContractError,verify_upstream,clone["upstream_documents"])
def test_assurance_cycle_rejected(clone):
 plan=clone["assurance_case_plan"]; plan["edges"].append({"source":"SN-010","target":"G-001","relation":"supported_by"}); graph,_,_=build(plan,{k:{} for n in plan["nodes"] for k in n["evidence_keys"]}); assert not graph["valid"] and not graph["acyclic"]
def test_assurance_unknown_node_rejected(clone):
 plan=clone["assurance_case_plan"]; plan["edges"][0]["target"]="MISSING"; pytest.raises(SafetyCaseError,build,plan,{})
def test_assurance_missing_evidence_fails_closed(clone):
 graph,_,trace=build(clone["assurance_case_plan"],{}); assert not graph["valid"] and not trace["complete"]
