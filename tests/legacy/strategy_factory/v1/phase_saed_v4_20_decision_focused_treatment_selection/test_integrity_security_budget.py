import copy,pytest
from saed_v4_decision_focused_treatment_selection.canonical import content_hash,canonical_bytes
from saed_v4_decision_focused_treatment_selection.certificates import verify_selection_certificate
from saed_v4_decision_focused_treatment_selection.errors import CertificateError,BudgetError,IntegrityError
from saed_v4_decision_focused_treatment_selection.security import assert_secure_payload,scan_payload
from saed_v4_decision_focused_treatment_selection.contracts import SelectionBudget
from saed_v4_decision_focused_treatment_selection.budget import BudgetLedger
from saed_v4_decision_focused_treatment_selection.integrity import verify_upstream_hashes,seal_registry
from saed_v4_decision_focused_treatment_selection.replay import replay_receipt,assert_future_suffix_invariance

def test_canonical_order_independent():assert content_hash({'b':1,'a':2})==content_hash({'a':2,'b':1})
def test_certificate_tamper_rejected(golden_result):
 c=copy.deepcopy(golden_result['certificate']);c['context_id']='tampered'
 with pytest.raises(CertificateError):verify_selection_certificate(c)
def test_authority_escalation_certificate_rejected(golden_result):
 c=copy.deepcopy(golden_result['certificate']);c['decision_authority']=True;c['certificate_hash']=content_hash({k:v for k,v in c.items() if k!='certificate_hash'})
 with pytest.raises(CertificateError):verify_selection_certificate(c)
def test_security_scan_clean():assert assert_secure_payload({'safe':{'x':1}})
@pytest.mark.parametrize('key',['live_credentials','broker_password','broker_token','private_signing_key','protected_final_evidence','future_outcomes','order_sender'])
def test_security_scan_forbidden(key):
 assert scan_payload({key:'x'})
 with pytest.raises(ValueError):assert_secure_payload({key:'x'})
def test_hidden_evaluation_budget_forbidden(config):
 b=BudgetLedger(SelectionBudget.from_mapping(config['budget']))
 with pytest.raises(BudgetError):b.consume('hidden_evaluation_queries')
def test_protected_evidence_budget_forbidden(config):
 b=BudgetLedger(SelectionBudget.from_mapping(config['budget']))
 with pytest.raises(BudgetError):b.consume('protected_evidence_exposure')
def test_regular_budget_enforced(config):
 x=copy.deepcopy(config['budget']);x['max_contexts']=1;b=BudgetLedger(SelectionBudget.from_mapping(x));b.consume('contexts')
 with pytest.raises(BudgetError):b.consume('contexts')
def test_upstream_hashes(config):
 expected={'a':'1'};assert verify_upstream_hashes({'a':'1','b':'2'},expected)
 with pytest.raises(IntegrityError):verify_upstream_hashes({'a':'x'},expected)
def test_registry_deterministic():assert seal_registry([{'id':'b'},{'id':'a'}])==seal_registry([{'id':'a'},{'id':'b'}])
def test_replay_receipt_deterministic():assert replay_receipt({'a':1},{'b':2})==replay_receipt({'a':1},{'b':2})
def test_future_suffix_invariance_helper():assert assert_future_suffix_invariance({'a':1},{'a':1})
