from src.engine.tooling.strategy_factory.acl_os.acl_13.service import ACL13OneHourAssessmentService
from src.engine.tooling.strategy_factory.acl_os.acl_13.verify import verify_output
def test_build_reference(tmp_path,acl12,permit,assessment_request,budget):
    out=tmp_path/'out'; result=ACL13OneHourAssessmentService().build(acl12,permit,assessment_request,budget,out)
    assert result['passed'] and result['pilot_design_allowed'] and not result['pilot_execution_allowed']
    assert verify_output(out)['passed']
def test_replay_deterministic(tmp_path,acl12,permit,assessment_request,budget):
    a=tmp_path/'a'; b=tmp_path/'b'; svc=ACL13OneHourAssessmentService(); svc.build(acl12,permit,assessment_request,budget,a); svc.build(acl12,permit,assessment_request,budget,b)
    import json
    ra=json.loads((a/'report/one_hour_assessment_report.json').read_text()); rb=json.loads((b/'report/one_hour_assessment_report.json').read_text()); assert ra['report_digest']==rb['report_digest']
def test_output_marker(tmp_path,acl12,permit,assessment_request,budget):
    out=tmp_path/'out'; ACL13OneHourAssessmentService().build(acl12,permit,assessment_request,budget,out); assert (out/'.acl13_generated_root').is_file()
