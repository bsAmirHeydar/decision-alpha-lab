import copy, json, pytest
from src.engine.tooling.strategy_factory.lcm.lcm_01.authority import verify_permit
from src.engine.tooling.strategy_factory.lcm.lcm_01.event_ledger import verify
from src.engine.tooling.strategy_factory.lcm.lcm_01.errors import ContractViolation, IntegrityError

def test_authority_permit_denies_escalation(survey_root):
    v=json.loads((survey_root/'authority/authority_permit_snapshot.json').read_text())
    assert v['source_move_allowed'] is False and v['source_delete_allowed'] is False and v['runtime_authority_allowed'] is False

def test_tampered_permit_rejected(survey_root):
    v=json.loads((survey_root/'authority/authority_permit_snapshot.json').read_text()); v['source_delete_allowed']=True
    with pytest.raises(ContractViolation): verify_permit(v,v['baseline_id'],v['baseline_manifest_digest'],v['source_handoff_digest'])

def test_event_chain_verifies_and_tamper_fails(survey_root):
    v=json.loads((survey_root/'events/survey_event_ledger.json').read_text()); verify(v)
    bad=copy.deepcopy(v); bad['events'][1]['payload']['x']='tamper'
    with pytest.raises(IntegrityError): verify(bad)

def test_handoff_is_non_destructive(survey_root):
    v=json.loads((survey_root/'handoff/lcm01_to_lcm02_handoff.json').read_text())
    assert 'CLASSIFY_SURVEYED_ARTIFACTS' in v['allowed_actions']
    assert 'DELETE_SOURCE_FILE' in v['forbidden_actions']
