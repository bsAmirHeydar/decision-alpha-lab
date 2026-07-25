from tools.strategy_factory.acl_os.acl_13.service import ACL13OneHourAssessmentService
import json
def build(tmp_path,acl12,permit,assessment_request,budget):
    out=tmp_path/'out'; ACL13OneHourAssessmentService().build(acl12,permit,assessment_request,budget,out); return out
def test_decision_non_capital(tmp_path,acl12,permit,assessment_request,budget):
    d=json.loads((build(tmp_path,acl12,permit,assessment_request,budget)/'decision/one_hour_assessment_result.json').read_text()); assert d['capital_activation_allowed'] is False
def test_decision_no_validation(tmp_path,acl12,permit,assessment_request,budget):
    d=json.loads((build(tmp_path,acl12,permit,assessment_request,budget)/'decision/one_hour_assessment_result.json').read_text()); assert d['validation_claim_allowed'] is False
def test_handoff_type(tmp_path,acl12,permit,assessment_request,budget):
    h=json.loads((build(tmp_path,acl12,permit,assessment_request,budget)/'handoff/acl14_handoff.json').read_text()); assert h['handoff_type']=='ACL13_TO_ACL14'
def test_handoff_design_only(tmp_path,acl12,permit,assessment_request,budget):
    h=json.loads((build(tmp_path,acl12,permit,assessment_request,budget)/'handoff/acl14_handoff.json').read_text()); assert h['first_real_context_pilot_design_allowed'] and not h['first_real_context_pilot_execution_allowed']
def test_handoff_forbidden_actions(tmp_path,acl12,permit,assessment_request,budget):
    h=json.loads((build(tmp_path,acl12,permit,assessment_request,budget)/'handoff/acl14_handoff.json').read_text()); assert 'TREAT_TRIAGE_AS_VALIDATION' in h['forbidden_acl14_actions']
