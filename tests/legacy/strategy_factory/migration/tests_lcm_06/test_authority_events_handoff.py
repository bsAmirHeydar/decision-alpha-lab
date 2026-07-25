import json,copy,pytest
from tools.strategy_factory.lcm.lcm_06.authority import verify_permit
from tools.strategy_factory.lcm.lcm_06.errors import PolicyError
def test_permit_no_authority(framework_root):
    p=json.loads((framework_root/"authority/authority_permit.json").read_text());assert verify_permit(p,p["source_handoff_digest"]);assert not p["source_move_allowed"] and not p["capital_authority"]
def test_permit_escalation_rejected(framework_root):
    p=json.loads((framework_root/"authority/authority_permit.json").read_text());p["runtime_authority"]=True
    with pytest.raises(PolicyError): verify_permit(p,p["source_handoff_digest"])
def test_event_chain(framework_root):
    e=json.loads((framework_root/"events/framework_event_ledger.json").read_text());prev=None
    for i,x in enumerate(e["events"],1): assert x["sequence"]==i and x["previous_event_digest"]==prev;prev=x["event_digest"]
    assert prev==e["final_event_digest"]
def test_handoff_denials(framework_root):
    h=json.loads((framework_root/"handoff/lcm06_to_lcm07_handoff.json").read_text());assert not h["shared_engine_extraction_authorized"];assert "MERGE_WITHOUT_EQUIVALENCE" in h["forbidden_actions"]

def test_permit_identity_tamper_rejected(framework_root):
    p=json.loads((framework_root/"authority/authority_permit.json").read_text());p["permit_id"]="PERMIT_TAMPERED"
    with pytest.raises(PolicyError): verify_permit(p,p["source_handoff_digest"],p["topology_run_id"])

def test_permit_topology_binding_rejected(framework_root):
    p=json.loads((framework_root/"authority/authority_permit.json").read_text())
    with pytest.raises(PolicyError): verify_permit(p,p["source_handoff_digest"],"TOPOLOGY_WRONG")
