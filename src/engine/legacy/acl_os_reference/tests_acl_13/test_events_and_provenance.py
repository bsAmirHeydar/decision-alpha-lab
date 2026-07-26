import json,copy
from src.engine.tooling.strategy_factory.acl_os.acl_13.service import ACL13OneHourAssessmentService
from src.engine.tooling.strategy_factory.acl_os.acl_13.events import verify_event_ledger
def output(tmp_path,acl12,permit,assessment_request,budget):
    out=tmp_path/'out'; ACL13OneHourAssessmentService().build(acl12,permit,assessment_request,budget,out); return out
def test_event_chain(tmp_path,acl12,permit,assessment_request,budget):
    e=json.loads((output(tmp_path,acl12,permit,assessment_request,budget)/'events/one_hour_assessment_event_ledger.json').read_text()); assert verify_event_ledger(e)
def test_event_tamper_detected(tmp_path,acl12,permit,assessment_request,budget):
    e=json.loads((output(tmp_path,acl12,permit,assessment_request,budget)/'events/one_hour_assessment_event_ledger.json').read_text()); e['events'][1]['payload']['x']=1; assert not verify_event_ledger(e)
def test_provenance_reaches_acl12(tmp_path,acl12,permit,assessment_request,budget):
    p=json.loads((output(tmp_path,acl12,permit,assessment_request,budget)/'lineage/one_hour_assessment_provenance_graph.json').read_text()); assert p['reaches_acl12_security_readiness']
def test_no_validation_invention(tmp_path,acl12,permit,assessment_request,budget):
    p=json.loads((output(tmp_path,acl12,permit,assessment_request,budget)/'lineage/one_hour_assessment_provenance_graph.json').read_text()); assert p['validation_evidence_invented'] is False
